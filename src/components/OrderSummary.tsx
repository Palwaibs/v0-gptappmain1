import React from 'react';
import { useOrder } from '../contexts/OrderContext';
import { Check, Tag } from 'lucide-react';

const OrderSummary: React.FC = () => {
  const { state } = useOrder();
  
  if (!state.selectedPackage) return null;

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
    }).format(price);
  };

  const discount = state.selectedPackage.originalPrice 
    ? state.selectedPackage.originalPrice - state.selectedPackage.price
    : 0;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 sticky top-4">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Ringkasan Pesanan</h2>
      
      {/* Package Info */}
      <div className="border border-gray-200 rounded-lg p-4 mb-6">
        <h3 className="font-semibold text-gray-900 mb-2">{state.selectedPackage.name}</h3>
        <p className="text-sm text-gray-600 mb-3">Durasi: {state.selectedPackage.duration}</p>
        
        <div className="space-y-2">
          {state.selectedPackage.features.slice(0, 3).map((feature, index) => (
            <div key={index} className="flex items-center space-x-2">
              <Check className="h-4 w-4 text-green-500 flex-shrink-0" />
              <span className="text-sm text-gray-700">{feature}</span>
            </div>
          ))}
          {state.selectedPackage.features.length > 3 && (
            <p className="text-sm text-gray-500 italic">
              +{state.selectedPackage.features.length - 3} fitur lainnya
            </p>
          )}
        </div>
      </div>
      
      {/* Price Breakdown */}
      <div className="space-y-3 pb-4 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Harga Paket:</span>
          <span className="font-medium">
            {state.selectedPackage.originalPrice ? (
              <>
                <span className="line-through text-gray-400 text-sm mr-2">
                  {formatPrice(state.selectedPackage.originalPrice)}
                </span>
                {formatPrice(state.selectedPackage.price)}
              </>
            ) : (
              formatPrice(state.selectedPackage.price)
            )}
          </span>
        </div>
        
        {discount > 0 && (
          <div className="flex justify-between items-center text-green-600">
            <div className="flex items-center space-x-1">
              <Tag className="h-4 w-4" />
              <span>Diskon:</span>
            </div>
            <span className="font-medium">-{formatPrice(discount)}</span>
          </div>
        )}
      </div>
      
      {/* Total */}
      <div className="pt-4 mb-6">
        <div className="flex justify-between items-center">
          <span className="text-lg font-semibold text-gray-900">Total Pembayaran:</span>
          <span className="text-2xl font-bold text-blue-600">
            {formatPrice(state.selectedPackage.price)}
          </span>
        </div>
      </div>
      
      {/* Security Notice */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <Check className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-medium text-green-800 text-sm">Pembayaran Aman</p>
            <p className="text-green-700 text-xs mt-1">
              Transaksi dienkripsi SSL dan data Anda dilindungi sepenuhnya
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderSummary;
