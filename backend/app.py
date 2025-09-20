import os
import uuid
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import config
from models import db, Order, InvitationLog, Package, AdminAccount
from utils.validators import validate_order_data
from utils.tripay_client import get_tripay_client
from utils.email_service import send_payment_confirmation, send_admin_notification

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name=None):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    CORS(app, 
         origins=app.config['ALLOWED_ORIGINS'],
         allow_headers=['Content-Type', 'Authorization', 'Accept'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         supports_credentials=True)
    
    # Configure rate limiting
    limiter = Limiter(key_func=get_remote_address)
    limiter.init_app(app)
    
    # Initialize Celery (optional)
    celery = None
    if app.config.get('ENABLE_CELERY', False):
        try:
            from tasks import make_celery
            celery = make_celery(app)
        except Exception as e:
            logger.warning(f"Celery initialization failed: {str(e)}")
    
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'environment': config_name  # Added environment info
        })
    
    @app.route('/healthz', methods=['GET'])
    def healthz():
        """Alternative health check endpoint"""
        return health_check()

    
    @app.route('/api/orders', methods=['POST'])
    @limiter.limit("10 per minute")
    def create_order():
        """Create new order and initiate payment"""
        try:
            # Get request data
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Validate input data
            is_valid, errors, validated_data = validate_order_data(data)
            if not is_valid:
                return jsonify({'error': 'Validation failed', 'details': errors}), 400
            
            # Generate unique merchant_ref if not provided
            merchant_ref = validated_data.get('merchant_ref')
            if not merchant_ref:
                import time
                merchant_ref = f"INV-{int(time.time())}"
            
            # Get package information
            packages = app.config['PACKAGES']
            package = packages.get(validated_data['package_id'])
            
            if not package:
                return jsonify({'error': 'Invalid package_id'}), 400
            
            # Get amount from server-side package (security)
            amount = package['price']
            
            # Get payment method
            payment_method = validated_data.get('payment_method', 'QRIS')
            
            # Create order record
            order = Order(
                order_id=merchant_ref,
                customer_email=validated_data['customer_email'],
                full_name=validated_data.get('full_name', validated_data.get('name')),
                phone_number=validated_data.get('phone_number'),
                package_id=validated_data['package_id'],
                amount=amount,
                payment_status='pending',
                invitation_status='pending'
            )
            
            db.session.add(order)
            db.session.flush()  # Get the ID without committing
            
            # Create payment transaction
            tripay_client = get_tripay_client()
            payment_data = {
                'merchant_ref': merchant_ref,
                'amount': amount,
                'customer_email': validated_data['customer_email'],
                'customer_name': validated_data.get('full_name', validated_data.get('name', 'Customer')),
                'phone_number': validated_data.get('phone_number', validated_data.get('phone', '')),
                'package_id': validated_data['package_id'],
                'package_name': package['name']
            }
            
            payment_result = tripay_client.create_transaction(payment_data, method=payment_method)
            
            if not payment_result.get('success', False):
                db.session.rollback()
                logger.error(f"Tripay error: {payment_result.get('error', 'Unknown error')}")
                return jsonify({
                    'error': payment_result.get('error', 'Payment gateway error'),
                    'details': payment_result.get('details', {})
                }), 500
            
            # Update order with Tripay transaction details
            order.checkout_url = payment_result.get('checkout_url')
            order.payment_method = payment_result.get('payment_method')
            order.reference = payment_result.get('reference')
            
            db.session.commit()
            
            logger.info(f"Order created successfully: {merchant_ref}")
            
            return jsonify({
                'success': True,
                'order_id': merchant_ref,
                'reference': payment_result.get('reference'),
                'checkout_url': payment_result.get('checkout_url'),
                'qr_string': payment_result.get('qr_string'),
                'payment_method': payment_result.get('payment_method'),
                'amount': amount,
                'status': 'pending_payment'
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating order: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/orders/<order_id>/status', methods=['GET'])
    @limiter.limit("30 per minute")
    def get_order_status(order_id):
        """Get order status"""
        try:
            order = Order.query.filter_by(order_id=order_id).first()
            
            if not order:
                return jsonify({'error': 'Order not found'}), 404
            
            # Generate status message
            message = generate_status_message(order)
            
            return jsonify({
                'order_id': order.order_id,
                'payment_status': order.payment_status,
                'invitation_status': order.invitation_status,
                'message': message
            })
            
        except Exception as e:
            logger.error(f"Error getting order status: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/payment/webhook', methods=['POST'])
    def tripay_callback():
        """Handle Tripay payment callback"""
        try:
            # Get webhook data
            webhook_data = request.get_json()
            if not webhook_data:
                logger.error("No callback data received from Tripay")
                return jsonify({'error': 'No data'}), 400
            
            # Log callback data (without signature for security)
            safe_data = {k: v for k, v in webhook_data.items() if k != 'signature'}
            logger.info(f"Tripay callback received: {safe_data}")
            
            # Verify webhook signature
            tripay_client = get_tripay_client()
            
            merchant_ref = webhook_data.get('merchant_ref')
            reference = webhook_data.get('reference')
            status = webhook_data.get('status')
            total_amount = webhook_data.get('total_amount', webhook_data.get('amount'))
            
            if not all([merchant_ref, reference, status]):
                logger.error("Missing required callback fields")
                return jsonify({'error': 'Missing required fields'}), 400
            
            # Verify signature
            if not tripay_client.verify_callback_signature(webhook_data):
                logger.error(f"Invalid callback signature for order {merchant_ref}")
                logger.error(f"Callback body: {safe_data}")
                return jsonify({'error': 'Invalid signature'}), 401
            
            # Find order
            order = Order.query.filter_by(order_id=merchant_ref).first()
            if not order:
                logger.error(f"Order not found: {merchant_ref}")
                return jsonify({'error': 'Order not found'}), 404
            
            # Map Tripay status to our internal status
            status_mapping = {
                'PAID': 'paid',
                'EXPIRED': 'expired',
                'FAILED': 'failed',
                'UNPAID': 'pending'
            }
            
            new_status = status_mapping.get(status, 'pending')
            old_status = order.payment_status
            
            # Update order status
            order.payment_status = new_status
            order.updated_at = datetime.utcnow()
            
            # If payment is successful, trigger invitation process
            if new_status == 'paid' and old_status != 'paid':
                order.invitation_status = 'processing'
                
                # Send payment confirmation email
                try:
                    send_payment_confirmation(order)
                except Exception as e:
                    logger.error(f"Failed to send payment confirmation: {str(e)}")
                
                # Trigger invitation task
                if celery:
                    try:
                        from tasks import process_invitation_task
                        process_invitation_task.delay(order.id)
                        logger.info(f"Invitation task queued for order {merchant_ref}")
                    except Exception as e:
                        logger.error(f"Failed to queue invitation task: {str(e)}")
                        order.invitation_status = 'failed'
                else:
                    logger.info(f"Celery disabled, invitation task not queued for order {merchant_ref}")
            
            db.session.commit()
            
            logger.info(f"Tripay callback processed successfully for order {merchant_ref}: {old_status} -> {new_status}")
            
            return jsonify({'success': True}), 200
            
        except Exception as e:
            logger.error(f"Tripay callback processing error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/callback/tripay', methods=['POST'])
    def tripay_callback_endpoint():
        """Tripay callback endpoint with proper path"""
        return tripay_callback()
    
    @app.route('/api/packages', methods=['GET'])
    def get_packages():
        """Get available packages"""
        try:
            packages = app.config['PACKAGES']
            return jsonify({'packages': packages})
        except Exception as e:
            logger.error(f"Error getting packages: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/admin/orders', methods=['GET'])
    @limiter.limit("100 per hour")
    def admin_get_orders():
        """Admin endpoint to get orders (basic implementation)"""
        try:
            # In production, add proper authentication here
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 20, type=int), 100)
            
            orders = Order.query.order_by(Order.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            return jsonify({
                'orders': [order.to_dict() for order in orders.items],
                'total': orders.total,
                'pages': orders.pages,
                'current_page': page
            })
            
        except Exception as e:
            logger.error(f"Error getting admin orders: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    def generate_status_message(order):
        """Generate human-readable status message"""
        if order.payment_status == 'pending':
            return "Menunggu pembayaran. Silakan selesaikan pembayaran sesuai instruksi."
        elif order.payment_status == 'failed':
            return "Pembayaran gagal. Silakan coba lagi atau hubungi support."
        elif order.payment_status == 'expired':
            return "Pembayaran kedaluwarsa. Silakan buat pesanan baru."
        elif order.payment_status == 'paid':
            if order.invitation_status == 'pending':
                return "Pembayaran berhasil. Proses undangan akan segera dimulai."
            elif order.invitation_status == 'processing':
                return "Pembayaran berhasil. Undangan sedang diproses dan akan dikirim dalam 5-30 menit."
            elif order.invitation_status == 'sent':
                return f"Undangan ChatGPT Plus telah dikirim ke {order.customer_email}. Silakan cek inbox dan spam folder."
            elif order.invitation_status == 'failed':
                return "Pembayaran berhasil, namun ada kendala dalam pengiriman undangan. Tim support akan menghubungi Anda."
            elif order.invitation_status == 'manual_review_required':
                return "Pembayaran berhasil. Undangan memerlukan review manual. Tim support akan menghubungi Anda segera."
        
        return "Status tidak diketahui. Silakan hubungi support."
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({'error': 'Rate limit exceeded', 'message': str(e.description)}), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

def init_database(app):
    """Initialize database with default data"""
    with app.app_context():
        db.create_all()
        
        # Add default packages if they don't exist
        packages_config = app.config['PACKAGES']
        for package_id, package_data in packages_config.items():
            existing_package = Package.query.get(package_id)
            if not existing_package:
                package = Package(
                    id=package_id,
                    name=package_data['name'],
                    price=package_data['price'],
                    duration=package_data['duration'],
                    description=package_data['description']
                )
                db.session.add(package)
        
        db.session.commit()
        logger.info("Database initialized successfully")

if __name__ == '__main__':
    app = create_app()
    
    # Initialize database
    init_database(app)
    
    # Use environment variables for production deployment
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'production') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
