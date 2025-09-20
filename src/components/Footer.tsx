import React from 'react';
import { Shield, Mail, MessageCircle, CheckCircle, Clock, Award } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-900 text-white py-16" id="contact">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">ChatGPT Plus Legal</h3>
                <p className="text-blue-400">Hemat 92% - Garansi Penuh</p>
              </div>
            </div>
            <p className="text-gray-400 mb-4 max-w-md">
              Dapatkan akses ChatGPT Plus legal dengan harga terjangkau. 
              Sistem invite resmi, bukan sharing account.
            </p>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-green-400">
                <CheckCircle className="h-4 w-4" />
                <span className="text-sm">100% Legal</span>
              </div>
              <div className="flex items-center space-x-2 text-blue-400">
                <Clock className="h-4 w-4" />
                <span className="text-sm">Proses Cepat</span>
              </div>
              <div className="flex items-center space-x-2 text-yellow-400">
                <Award className="h-4 w-4" />
                <span className="text-sm">Garansi 7 Hari</span>
              </div>
            </div>
          </div>
          
          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-white mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <a href="#packages" className="text-gray-400 hover:text-blue-400 transition-colors text-sm">
                  Paket Harga
                </a>
              </li>
              <li>
                <a href="#faq" className="text-gray-400 hover:text-blue-400 transition-colors text-sm">
                  FAQ
                </a>
              </li>
              <li>
                <a href="#testimonials" className="text-gray-400 hover:text-blue-400 transition-colors text-sm">
                  Testimoni
                </a>
              </li>
            </ul>
          </div>
          
          {/* Contact */}
          <div>
            <h4 className="font-semibold text-white mb-4">Hubungi Kami</h4>
            <div className="space-y-3">
              <a 
                href="mailto:support@chatgptplus-legal.com" 
                className="flex items-center space-x-2 text-gray-400 hover:text-blue-400 transition-colors"
              >
                <Mail className="h-4 w-4" />
                <span className="text-sm">support@chatgptplus-legal.com</span>
              </a>
              <a 
                href="https://wa.me/6281234567890" 
                className="flex items-center space-x-2 text-gray-400 hover:text-green-400 transition-colors"
              >
                <MessageCircle className="h-4 w-4" />
                <span className="text-sm">WhatsApp Support</span>
              </a>
            </div>
          </div>
        </div>
        
        <div className="border-t border-slate-700/50 pt-8 text-center">
          <p className="text-gray-400 text-sm mb-4">
            &copy; 2025 ChatGPT Plus Legal. All rights reserved.
          </p>
          <div className="inline-flex items-center space-x-2 bg-green-500/20 text-green-400 px-4 py-2 rounded-full text-sm">
            <Shield className="h-4 w-4" />
            <span>Terpercaya oleh 2,000+ pengguna Indonesia</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
