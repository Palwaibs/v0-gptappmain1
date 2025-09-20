import React from 'react';
import { Package } from '../contexts/OrderContext';
import { Check, Star, Crown, ArrowRight, Users, User } from 'lucide-react';

interface PackageCardProps {
  package: Package;
  onSelect: () => void;
}

const PackageCard: React.FC<PackageCardProps> = ({ package: pkg, onSelect }) => {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
    }).format(price);
  };

  const discount = pkg.originalPrice 
    ? Math.round(((pkg.originalPrice - pkg.price) / pkg.originalPrice) * 100)
    : 0;

  const isTeamPackage = pkg.id === 'team_package';

  return (
    <div className={`relative bg-white rounded-lg shadow-sm hover:shadow-md transition-all duration-300 border overflow-hidden ${
      pkg.popular 
        ? 'border-blue-200 bg-gradient-to-br from-blue-50/50 to-indigo-50/50' 
        : 'border-gray-200 hover:border-blue-200'
    }`}>
      
      {/* Popular Badge */}
      {pkg.popular && (
        <div className="absolute top-3 right-3">
          <div className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white px-2 py-1 rounded-full text-xs font-bold">
            <span>Populer</span>
          </div>
        </div>
      )}

      <div className="p-4">
        {/* Header */}
        <div className="text-center mb-3">
          <div className={`inline-flex items-center justify-center w-12 h-12 rounded-xl mb-3 shadow-md ${
            pkg.popular 
              ? 'bg-gradient-to-br from-blue-500 to-indigo-600' 
              : 'bg-gradient-to-br from-gray-500 to-gray-600'
          }`}>
            {isTeamPackage ? (
              <Users className="h-6 w-6 text-white" />
            ) : (
              <User className="h-6 w-6 text-white" />
            )}
          </div>
          
          <h3 className="text-base font-bold text-gray-900 mb-1">{pkg.name}</h3>
          <p className="text-gray-600 text-xs font-medium">{pkg.duration}</p>
          
          {isTeamPackage && (
            <div className="mt-2 inline-flex items-center space-x-1 bg-purple-100 text-purple-700 px-2 py-1 rounded-full text-xs font-semibold">
              <Users className="h-3 w-3" />
              <span>Untuk 5 Orang</span>
            </div>
          )}
        </div>

        {/* Pricing */}
        <div className="text-center mb-3">
          {pkg.originalPrice && (
            <div className="flex items-center justify-center space-x-2 mb-2">
              <span className="text-sm text-gray-400 line-through">
                {formatPrice(pkg.originalPrice)}
              </span>
              <div className="bg-red-100 text-red-600 px-2 py-1 rounded-full text-xs font-bold">
                Hemat {discount}%
              </div>
            </div>
          )}
          
          <div className="flex items-baseline justify-center space-x-1">
            <span className="text-xs text-gray-500">Rp</span>
            <span className={`text-3xl font-black ${
              pkg.popular ? 'text-blue-600' : 'text-gray-900'
            }`}>
              {Math.floor(pkg.price / 1000)}
            </span>
            <span className="text-lg text-gray-500">k</span>
          </div>
          
          <p className="text-gray-500 mt-1 text-xs font-medium">per bulan</p>
          
          {isTeamPackage && (
            <p className="text-xs text-purple-600 font-semibold mt-1">
              Hanya Rp 19k per orang
            </p>
          )}
        </div>
        
        {/* Features */}
        <div className="space-y-1.5 mb-3">
          {pkg.features.map((feature, index) => (
            <div key={index} className="flex items-start space-x-3">
              <div className={`flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center mt-0.5 ${
                pkg.popular 
                  ? 'bg-blue-100' 
                  : 'bg-green-100'
              }`}>
                <Check className={`h-3 w-3 ${
                  pkg.popular ? 'text-blue-600' : 'text-green-600'
                }`} />
              </div>
              <span className="text-gray-700 text-xs">
                {feature}
              </span>
            </div>
          ))}
        </div>
        
        {/* CTA Button */}
        <button
          onClick={onSelect}
          className={`group w-full py-2.5 px-4 rounded-lg font-bold text-sm transition-all duration-300 flex items-center justify-center space-x-2 shadow-md ${
            pkg.popular 
              ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-500 hover:to-indigo-500 hover:shadow-blue-500/25'
              : 'bg-gradient-to-r from-gray-700 to-gray-800 text-white hover:from-gray-600 hover:to-gray-700 hover:shadow-gray-500/25'
          }`}
        >
          <span>{pkg.buttonText}</span>
          <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
        </button>

        {/* Trust Badge */}
        <div className="mt-2 text-center">
          <div className="inline-flex items-center space-x-2 text-sm text-gray-500">
            <div className="flex -space-x-1">
              <div className="w-4 h-4 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-full border-2 border-white"></div>
              <div className="w-4 h-4 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full border-2 border-white"></div>
              <div className="w-4 h-4 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full border-2 border-white"></div>
            </div>
            <span className="font-medium text-xs">2,000+ pengguna</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PackageCard;
