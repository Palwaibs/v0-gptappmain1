// Mock API Service for preview/demo purposes
export interface CreateOrderRequest {
  customer_email: string;
  package_id: string;
  full_name: string;
  phone_number: string;
}

export interface CreateOrderResponse {
  order_id: string;
  payment_url: string;
  status: string;
}

export interface OrderStatusResponse {
  order_id: string;
  payment_status: 'pending' | 'paid' | 'failed' | 'expired';
  invitation_status: 'pending' | 'processing' | 'sent' | 'failed' | 'manual_review_required';
  message: string;
}

class MockApiService {
  private orders: Map<string, any> = new Map();
  private orderCounter = 1;

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private generateOrderId(): string {
    return `ORD${String(this.orderCounter++).padStart(8, '0')}`;
  }

  async createOrder(orderData: CreateOrderRequest): Promise<CreateOrderResponse> {
    // Simulate API delay
    await this.delay(1000);

    // Simulate validation errors occasionally
    if (Math.random() < 0.1) {
      throw new Error('Email format tidak valid');
    }

    const orderId = this.generateOrderId();
    
    // Store order data
    this.orders.set(orderId, {
      ...orderData,
      order_id: orderId,
      payment_status: 'pending',
      invitation_status: 'pending',
      created_at: new Date().toISOString()
    });

    // Simulate payment URL (in real app, this would be from Midtrans)
    const mockCheckoutUrl = `/confirmation?order_id=${orderId}`;

    return {
      order_id: orderId,
      checkout_url: mockCheckoutUrl,
      reference: `TF${orderId}`,
      status: 'pending_payment'
    };
  }

  async getOrderStatus(orderId: string): Promise<OrderStatusResponse> {
    // Simulate API delay
    await this.delay(500);

    console.log('MockApiService - getOrderStatus called with orderId:', orderId);
    console.log('MockApiService - available orders:', Array.from(this.orders.keys()));

    const order = this.orders.get(orderId);
    
    if (!order) {
      console.log('MockApiService - Order not found for orderId:', orderId);
      throw new Error('Order tidak ditemukan');
    }

    // Simulate payment processing flow
    const now = new Date();
    const createdAt = new Date(order.created_at);
    const minutesElapsed = (now.getTime() - createdAt.getTime()) / (1000 * 60);

    let paymentStatus = order.payment_status;
    let invitationStatus = order.invitation_status;
    let message = '';

    // Simulate payment success after 30 seconds
    if (minutesElapsed > 0.5 && paymentStatus === 'pending') {
      paymentStatus = 'paid';
      invitationStatus = 'processing';
      
      // Update stored order
      this.orders.set(orderId, {
        ...order,
        payment_status: paymentStatus,
        invitation_status: invitationStatus
      });
    }

    // Simulate invitation sent after 2 minutes
    if (minutesElapsed > 2 && paymentStatus === 'paid' && invitationStatus === 'processing') {
      invitationStatus = 'sent';
      
      // Update stored order
      this.orders.set(orderId, {
        ...order,
        invitation_status: invitationStatus
      });
    }

    // Generate appropriate message
    if (paymentStatus === 'pending') {
      message = 'Menunggu pembayaran. Silakan selesaikan pembayaran sesuai instruksi.';
    } else if (paymentStatus === 'paid') {
      if (invitationStatus === 'processing') {
        message = 'Pembayaran berhasil. Undangan sedang diproses dan akan dikirim dalam 5-30 menit.';
      } else if (invitationStatus === 'sent') {
        message = `Undangan ChatGPT Plus telah dikirim ke ${order.customer_email}. Silakan cek inbox dan spam folder.`;
      }
    }

    return {
      order_id: orderId,
      payment_status: paymentStatus,
      invitation_status: invitationStatus,
      message
    };
  }

  // Method to simulate payment completion (for demo purposes)
  simulatePaymentSuccess(orderId: string): void {
    const order = this.orders.get(orderId);
    if (order) {
      this.orders.set(orderId, {
        ...order,
        payment_status: 'paid',
        invitation_status: 'processing'
      });
    }
  }

  // Method to simulate invitation sent (for demo purposes)
  simulateInvitationSent(orderId: string): void {
    const order = this.orders.get(orderId);
    if (order) {
      this.orders.set(orderId, {
        ...order,
        invitation_status: 'sent'
      });
    }
  }
}

export const mockApiService = new MockApiService();
