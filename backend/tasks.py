import os
import logging
from datetime import datetime, timedelta
from celery import Celery
from celery import shared_task
from flask import current_app
from models import db, Order, InvitationLog
from automation.chatgpt_inviter import create_inviter
from utils.email_service import send_invitation_confirmation, send_admin_notification

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_celery(app):
    """Create Celery instance and configure it with Flask app"""
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

# This will be initialized in app.py
celery = None

@shared_task(bind=True, max_retries=3, default_retry_delay=300)
def process_invitation_task(self, order_id):
    """
    Celery task to process ChatGPT invitation
    
    Args:
        order_id (int): The order ID to process
    
    Returns:
        dict: Result of the invitation process
    """
    try:
        logger.info(f"Starting invitation process for order {order_id}")
        
        # Get order from database
        order = Order.query.get(order_id)
        if not order:
            logger.error(f"Order {order_id} not found")
            return {'success': False, 'error': 'Order not found'}
        
        # Check if order is paid
        if order.payment_status != 'paid':
            logger.error(f"Order {order_id} is not paid. Status: {order.payment_status}")
            return {'success': False, 'error': 'Order is not paid'}
        
        # Update invitation status to processing
        order.invitation_status = 'processing'
        db.session.commit()
        
        # Create invitation log entry
        log_entry = InvitationLog(
            order_id=order.id,
            status='processing',
            retry_count=self.request.retries
        )
        db.session.add(log_entry)
        db.session.commit()
        
        # Get configuration
        team_url = current_app.config.get('CHATGPT_ADMIN_URL', 'https://chatgpt.com/admin?tab=members')
        
        # Create inviter instance
        inviter = create_inviter(
            headless=current_app.config.get('SELENIUM_HEADLESS', True),
            timeout=current_app.config.get('SELENIUM_TIMEOUT', 30)
        )
        
        # Process invitation
        success = inviter.process_invitation(member_email=order.customer_email, team_url=team_url)
        
        if success:
            # Update order status
            order.invitation_status = 'sent'
            order.updated_at = datetime.utcnow()
            
            # Update log
            log_entry.status = 'success'
            
            db.session.commit()
            
            # Send confirmation email to customer
            try:
                send_invitation_confirmation(order)
                logger.info(f"Confirmation email sent to {order.customer_email}")
            except Exception as e:
                logger.error(f"Failed to send confirmation email: {str(e)}")
            
            logger.info(f"Invitation process completed successfully for order {order_id}")
            return {
                'success': True,
                'order_id': order.order_id,
                'customer_email': order.customer_email
            }
        
        else:
            # Invitation failed, determine if we should retry
            error_msg = f"Invitation failed for order {order_id}"
            logger.error(error_msg)
            
            # Update log
            log_entry.status = 'failure'
            log_entry.error_message = error_msg
            
            # Check retry count
            if self.request.retries < self.max_retries:
                # Schedule retry with exponential backoff
                retry_delay = 300 * (2 ** self.request.retries)  # 5min, 10min, 20min
                logger.info(f"Scheduling retry {self.request.retries + 1} for order {order_id} in {retry_delay} seconds")
                
                db.session.commit()
                raise self.retry(countdown=retry_delay)
            else:
                # Max retries reached, mark as failed
                order.invitation_status = 'manual_review_required'
                db.session.commit()
                
                # Send admin notification
                try:
                    send_admin_notification(
                        subject=f"Manual Review Required - Order {order.order_id}",
                        message=f"Invitation failed for order {order.order_id} after {self.max_retries} retries. Customer email: {order.customer_email}",
                        order=order
                    )
                except Exception as e:
                    logger.error(f"Failed to send admin notification: {str(e)}")
                
                return {
                    'success': False,
                    'error': 'Max retries reached, manual review required',
                    'order_id': order.order_id
                }
    
    except Exception as e:
        logger.error(f"Unexpected error in invitation process for order {order_id}: {str(e)}")
        
        try:
            # Update order and log
            order = Order.query.get(order_id)
            if order:
                order.invitation_status = 'failed'
                
                log_entry = InvitationLog(
                    order_id=order.id,
                    status='failure',
                    error_message=str(e),
                    retry_count=self.request.retries
                )
                db.session.add(log_entry)
                db.session.commit()
        except Exception as db_error:
            logger.error(f"Failed to update database after error: {str(db_error)}")
        
        # Retry if possible
        if self.request.retries < self.max_retries:
            retry_delay = 300 * (2 ** self.request.retries)
            raise self.retry(countdown=retry_delay, exc=e)
        
        return {'success': False, 'error': str(e)}

@shared_task
def cleanup_expired_orders():
    """Clean up expired orders and update their status"""
    try:
        logger.info("Starting cleanup of expired orders")
        
        # Find orders that are pending payment for more than 24 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        expired_orders = Order.query.filter(
            Order.payment_status == 'pending',
            Order.created_at < cutoff_time
        ).all()
        
        for order in expired_orders:
            order.payment_status = 'expired'
            order.updated_at = datetime.utcnow()
            
            logger.info(f"Marked order {order.order_id} as expired")
        
        db.session.commit()
        logger.info(f"Cleanup completed. {len(expired_orders)} orders marked as expired")
        
        return {'success': True, 'expired_count': len(expired_orders)}
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        return {'success': False, 'error': str(e)}

@shared_task
def retry_failed_invitations():
    """Retry failed invitations that might be recoverable"""
    try:
        logger.info("Starting retry of failed invitations")
        
        # Find orders with failed invitations from the last 6 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=6)
        failed_orders = Order.query.filter(
            Order.invitation_status == 'failed',
            Order.payment_status == 'paid',
            Order.updated_at > cutoff_time
        ).all()
        
        retry_count = 0
        for order in failed_orders:
            # Check if we haven't already retried too many times
            log_count = InvitationLog.query.filter_by(order_id=order.id).count()
            
            if log_count < 5:  # Max 5 total attempts
                logger.info(f"Retrying invitation for order {order.order_id}")
                process_invitation_task.delay(order.id)
                retry_count += 1
        
        logger.info(f"Retry process completed. {retry_count} invitations queued for retry")
        
        return {'success': True, 'retry_count': retry_count}
        
    except Exception as e:
        logger.error(f"Error during retry process: {str(e)}")
        return {'success': False, 'error': str(e)}

# Periodic tasks configuration
def setup_periodic_tasks(sender, **kwargs):
    """Setup periodic tasks - only if Celery is enabled"""
    if not current_app.config.get('ENABLE_CELERY', False):
        return
        
    # Cleanup expired orders every hour
    sender.add_periodic_task(
        3600.0,  # 1 hour
        cleanup_expired_orders.s(),
        name='cleanup expired orders'
    )
    
    # Retry failed invitations every 2 hours
    sender.add_periodic_task(
        7200.0,  # 2 hours
        retry_failed_invitations.s(),
        name='retry failed invitations'
    )

# Only register if Celery is enabled
try:
    from flask import current_app
    if current_app and current_app.config.get('ENABLE_CELERY', False):
        from celery.signals import after_configure
        after_configure.connect(setup_periodic_tasks)
except:
    pass
def setup_periodic_tasks(sender, **kwargs):
    """Setup periodic tasks"""
    
    # Cleanup expired orders every hour
    sender.add_periodic_task(
        3600.0,  # 1 hour
        cleanup_expired_orders.s(),
        name='cleanup expired orders'
    )
    
    # Retry failed invitations every 2 hours
    sender.add_periodic_task(
        7200.0,  # 2 hours
        retry_failed_invitations.s(),
        name='retry failed invitations'
    )
