import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from flask import current_app, render_template_string

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.enabled = current_app.config.get('EMAIL_ENABLED', False)
        self.api_key = current_app.config.get('SENDGRID_API_KEY')
        self.from_email = current_app.config.get('FROM_EMAIL')
        self.sg = SendGridAPIClient(api_key=self.api_key) if self.api_key and self.enabled else None
    
    def send_email(self, to_email, subject, html_content, text_content=None):
        """Send email using SendGrid"""
        if not self.enabled:
            logger.info(f"Email disabled - would send to {to_email}: {subject}")
            return True
        
        if not self.sg:
            logger.error("SendGrid not configured but email is enabled")
            return False
        
        try:
            from_email = Email(self.from_email)
            to_email = To(to_email)
            
            if not text_content:
                # Create text version from HTML
                import re
                text_content = re.sub('<[^<]+?>', '', html_content)
            
            mail = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                html_content=Content("text/html", html_content),
                plain_text_content=Content("text/plain", text_content)
            )
            
            response = self.sg.send(mail)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email. Status code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False

def get_email_service():
    """Factory function to get email service instance"""
    return EmailService()

def send_invitation_confirmation(order):
    """Send invitation confirmation email to customer"""
    try:
        email_service = get_email_service()
        
        # Get package info
        packages = current_app.config.get('PACKAGES', {})
        package = packages.get(order.package_id, {})
        
        # Email template
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>ChatGPT Plus Invitation Sent</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #4F46E5; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background: #f9f9f9; }
                .footer { padding: 20px; text-align: center; font-size: 12px; color: #666; }
                .button { display: inline-block; padding: 12px 24px; background: #4F46E5; color: white; text-decoration: none; border-radius: 5px; }
                .success { background: #10B981; color: white; padding: 15px; border-radius: 5px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 ChatGPT Plus Invitation Sent!</h1>
                </div>
                
                <div class="content">
                    <div class="success">
                        <strong>✅ Success!</strong> Your ChatGPT Plus invitation has been sent successfully.
                    </div>
                    
                    <h2>Hello {{ customer_name }},</h2>
                    
                    <p>Great news! Your ChatGPT Plus invitation has been sent to <strong>{{ customer_email }}</strong>.</p>
                    
                    <h3>Order Details:</h3>
                    <ul>
                        <li><strong>Order ID:</strong> {{ order_id }}</li>
                        <li><strong>Package:</strong> {{ package_name }}</li>
                        <li><strong>Duration:</strong> {{ package_duration }}</li>
                        <li><strong>Amount Paid:</strong> Rp {{ amount }}</li>
                    </ul>
                    
                    <h3>Next Steps:</h3>
                    <ol>
                        <li>Check your email inbox (including spam/junk folder)</li>
                        <li>Look for an invitation email from ChatGPT Team</li>
                        <li>Click the invitation link to join the team</li>
                        <li>Start enjoying ChatGPT Plus features!</li>
                    </ol>
                    
                    <p><strong>Note:</strong> The invitation email may take a few minutes to arrive. If you don't receive it within 30 minutes, please contact our support team.</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://wa.me/6281234567890" class="button">Contact Support</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Thank you for choosing our ChatGPT Plus service!</p>
                    <p>If you have any questions, feel free to contact our support team.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Render template
        html_content = render_template_string(
            html_template,
            customer_name=order.full_name or 'Valued Customer',
            customer_email=order.customer_email,
            order_id=order.order_id,
            package_name=package.get('name', 'ChatGPT Plus'),
            package_duration=package.get('duration', '1 Month'),
            amount=f"{int(order.amount):,}"
        )
        
        subject = f"✅ ChatGPT Plus Invitation Sent - Order {order.order_id}"
        
        return email_service.send_email(order.customer_email, subject, html_content)
        
    except Exception as e:
        logger.error(f"Failed to send invitation confirmation: {str(e)}")
        return False

def send_admin_notification(subject, message, order=None):
    """Send notification to admin"""
    try:
        admin_email = current_app.config.get('ADMIN_EMAIL')
        if not admin_email:
            logger.warning("Admin email not configured")
            return False
        
        email_service = get_email_service()
        
        # Admin notification template
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Admin Notification</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #EF4444; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background: #f9f9f9; }
                .alert { background: #FEF2F2; border: 1px solid #FECACA; padding: 15px; border-radius: 5px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚨 Admin Notification</h1>
                </div>
                
                <div class="content">
                    <div class="alert">
                        <h3>{{ subject }}</h3>
                        <p>{{ message }}</p>
                    </div>
                    
                    {% if order %}
                    <h3>Order Details:</h3>
                    <ul>
                        <li><strong>Order ID:</strong> {{ order.order_id }}</li>
                        <li><strong>Customer Email:</strong> {{ order.customer_email }}</li>
                        <li><strong>Package:</strong> {{ order.package_id }}</li>
                        <li><strong>Payment Status:</strong> {{ order.payment_status }}</li>
                        <li><strong>Invitation Status:</strong> {{ order.invitation_status }}</li>
                        <li><strong>Created:</strong> {{ order.created_at }}</li>
                        <li><strong>Updated:</strong> {{ order.updated_at }}</li>
                    </ul>
                    {% endif %}
                    
                    <p><strong>Timestamp:</strong> {{ timestamp }}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        from datetime import datetime
        html_content = render_template_string(
            html_template,
            subject=subject,
            message=message,
            order=order,
            timestamp=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        )
        
        return email_service.send_email(admin_email, f"[ADMIN] {subject}", html_content)
        
    except Exception as e:
        logger.error(f"Failed to send admin notification: {str(e)}")
        return False

def send_payment_confirmation(order):
    """Send payment confirmation email to customer"""
    try:
        email_service = get_email_service()
        
        # Get package info
        packages = current_app.config.get('PACKAGES', {})
        package = packages.get(order.package_id, {})
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Payment Confirmation</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #10B981; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background: #f9f9f9; }
                .success { background: #D1FAE5; border: 1px solid #A7F3D0; padding: 15px; border-radius: 5px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💳 Payment Confirmed</h1>
                </div>
                
                <div class="content">
                    <div class="success">
                        <strong>✅ Payment Successful!</strong> Your payment has been processed successfully.
                    </div>
                    
                    <h2>Hello {{ customer_name }},</h2>
                    
                    <p>Thank you for your payment! Your ChatGPT Plus invitation is being processed and will be sent to your email shortly.</p>
                    
                    <h3>Order Details:</h3>
                    <ul>
                        <li><strong>Order ID:</strong> {{ order_id }}</li>
                        <li><strong>Package:</strong> {{ package_name }}</li>
                        <li><strong>Amount Paid:</strong> Rp {{ amount }}</li>
                        <li><strong>Payment Date:</strong> {{ payment_date }}</li>
                    </ul>
                    
                    <p><strong>What's Next?</strong></p>
                    <p>Your ChatGPT Plus invitation will be sent to <strong>{{ customer_email }}</strong> within 5-30 minutes. Please check your inbox and spam folder.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        html_content = render_template_string(
            html_template,
            customer_name=order.full_name or 'Valued Customer',
            customer_email=order.customer_email,
            order_id=order.order_id,
            package_name=package.get('name', 'ChatGPT Plus'),
            amount=f"{int(order.amount):,}",
            payment_date=order.updated_at.strftime('%Y-%m-%d %H:%M:%S') if order.updated_at else 'N/A'
        )
        
        subject = f"💳 Payment Confirmed - Order {order.order_id}"
        
        return email_service.send_email(order.customer_email, subject, html_content)
        
    except Exception as e:
        logger.error(f"Failed to send payment confirmation: {str(e)}")
        return False
