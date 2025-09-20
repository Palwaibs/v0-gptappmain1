import React from 'react';
import { Star, Quote, CheckCircle, TrendingUp } from 'lucide-react';

const testimonials = [
  {
    name: 'Sarah Putri',
    role: 'Content Creator',
    company: 'Digital Agency',
    content: 'Awalnya ragu karena harganya murah banget. Tapi ternyata beneran dapat invite resmi dan berfungsi sempurna! Sudah 3 bulan langganan di sini, sangat puas.',
    rating: 5,
    avatar: 'https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&fit=crop',
    verified: true,
    savings: 'Hemat Rp 275k/bulan'
  },
  {
    name: 'Budi Santoso',
    role: 'Startup Founder',
    company: 'Tech Startup',
    content: 'Tim kami butuh ChatGPT Plus tapi budget terbatas. Paket tim di sini sangat membantu, semua anggota dapat akses pribadi dengan harga yang sangat terjangkau.',
    rating: 5,
    avatar: 'https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&fit=crop',
    verified: true,
    savings: 'Hemat Rp 1.2jt/bulan'
  },
  {
    name: 'Maya Sari',
    role: 'Freelancer',
    company: 'Digital Marketing',
    content: 'Customer servicenya responsif banget. Pas ada masalah teknis, langsung dibantu sampai selesai. Garansi uang kembali juga beneran ada. Recommended!',
    rating: 5,
    avatar: 'https://images.pexels.com/photos/1043471/pexels-photo-1043471.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&fit=crop',
    verified: true,
    savings: 'Hemat Rp 275k/bulan'
  }
];

const TestimonialSection: React.FC = () => {
  return (
    <section className="py-12 bg-white relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(59,130,246,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.03)_1px,transparent_1px)] bg-[size:40px_40px]"></div>
      
      <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-600 px-4 py-2 rounded-full text-sm font-semibold mb-4">
            <Star className="h-4 w-4 fill-current" />
            <span>Testimoni Pelanggan</span>
          </div>
          
          <h2 className="text-2xl md:text-3xl font-black text-gray-900 mb-4">
            Apa Kata <span className="text-blue-600">Pelanggan Kami</span>
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Testimoni dari 2,000+ pelanggan yang sudah merasakan manfaatnya
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="group relative">
              {/* Card */}
              <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-gray-100 hover:border-blue-200 relative overflow-hidden">
                
                {/* Background Gradient */}
                <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-blue-500/5 to-indigo-500/5 rounded-full -translate-y-10 translate-x-10"></div>
                
                {/* Quote Icon */}
                <div className="relative mb-4">
                  <Quote className="h-6 w-6 text-blue-400 opacity-30 absolute -top-1 -left-1" />
                </div>
                
                {/* Rating */}
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                  ))}
                </div>
                
                {/* Content */}
                <p className="text-gray-700 mb-4 leading-relaxed relative z-10 text-sm">
                  "{testimonial.content}"
                </p>
                
                {/* Savings Badge */}
                <div className="mb-4">
                  <div className="inline-flex items-center space-x-1 bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-semibold">
                    <TrendingUp className="h-3 w-3" />
                    <span>{testimonial.savings}</span>
                  </div>
                </div>
                
                {/* Author */}
                <div className="flex items-center space-x-4">
                  <div className="relative">
                    <img
                      src={testimonial.avatar}
                      alt={testimonial.name}
                      className="w-10 h-10 rounded-full object-cover ring-2 ring-blue-100"
                    />
                    {testimonial.verified && (
                      <div className="absolute -bottom-1 -right-1 bg-blue-500 rounded-full p-1">
                        <CheckCircle className="h-2 w-2 text-white" />
                      </div>
                    )}
                  </div>
                  <div>
                    <h4 className="font-bold text-gray-900 text-sm">{testimonial.name}</h4>
                    <p className="text-sm text-gray-600">{testimonial.role}</p>
                    <p className="text-xs text-blue-600 font-medium">{testimonial.company}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
};

export default TestimonialSection;
