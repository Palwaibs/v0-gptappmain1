import React from 'react';
import { mockApiService } from '../services/mockApiService';
import { Settings, Zap, CheckCircle } from 'lucide-react';

interface DemoControlsProps {
  orderId?: string;
  onRefresh?: () => void;
}

const DemoControls: React.FC<DemoControlsProps> = ({ orderId, onRefresh }) => {
  const USE_MOCK_API = true; // Force demo mode for preview

  if (!USE_MOCK_API || !orderId) {
    return null;
  }

  const handleSimulatePayment = () => {
    mockApiService.simulatePaymentSuccess(orderId);
    if (onRefresh) {
      setTimeout(onRefresh, 500);
    }
  };

  const handleSimulateInvitation = () => {
    mockApiService.simulateInvitationSent(orderId);
    if (onRefresh) {
      setTimeout(onRefresh, 500);
    }
  };

  return (
    <div className="fixed bottom-4 right-4 bg-white rounded-lg shadow-lg border border-gray-200 p-4 max-w-sm">
      <div className="flex items-center space-x-2 mb-3">
        <Settings className="h-5 w-5 text-blue-600" />
        <h3 className="font-semibold text-gray-900">Demo Controls</h3>
      </div>
      
      <p className="text-sm text-gray-600 mb-4">
        Gunakan tombol di bawah untuk mensimulasikan proses pembayaran dan invite:
      </p>
      
      <div className="space-y-2">
        <button
          onClick={handleSimulatePayment}
          className="w-full flex items-center justify-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm"
        >
          <Zap className="h-4 w-4" />
          <span>Simulasi Pembayaran Sukses</span>
        </button>
        
        <button
          onClick={handleSimulateInvitation}
          className="w-full flex items-center justify-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm"
        >
          <CheckCircle className="h-4 w-4" />
          <span>Simulasi Invite Terkirim</span>
        </button>
      </div>
      
      <p className="text-xs text-gray-500 mt-3">
        * Mode demo - tidak ada pembayaran atau invite yang sebenarnya
      </p>
    </div>
  );
};

export default DemoControls;
