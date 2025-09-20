import React, { useState } from 'react';
import { ChevronDown, ChevronUp, HelpCircle, Shield, CheckCircle } from 'lucide-react';

const faqs = [
  {
    question: 'Apakah sistem ini benar-benar legal dan aman?',
    answer: 'Ya, 100% legal. Kami menggunakan sistem invite resmi dari OpenAI, bukan account sharing. Setiap pelanggan mendapat invite pribadi ke email mereka sendiri. Metode ini sepenuhnya sesuai dengan terms of service OpenAI.',
    category: 'legal'
  },
  {
    question: 'Bagaimana bisa harganya jauh lebih murah dari resmi?',
    answer: 'Kami mendapat harga khusus melalui kemitraan dengan distributor resmi dan volume pembelian yang besar. Ini memungkinkan kami memberikan harga yang sangat kompetitif sambil tetap menjaga kualitas layanan.',
    category: 'pricing'
  },
  {
    question: 'Berapa lama proses aktivasi setelah pembayaran?',
    answer: 'Setelah pembayaran dikonfirmasi, invite biasanya dikirim dalam 1-6 jam. Pada jam kerja, prosesnya bisa lebih cepat. Kami bekerja 24/7 untuk memastikan proses yang cepat.',
    category: 'process'
  },
  {
    question: 'Apakah ada garansi jika tidak berfungsi?',
    answer: 'Ya, kami memberikan garansi uang kembali 100% dalam 7 hari pertama jika Anda mengalami masalah atau tidak puas dengan layanan. Tidak ada pertanyaan yang rumit, proses refund sangat mudah.',
    category: 'guarantee'
  },
  {
    question: 'Apakah bisa diperpanjang setelah masa aktif habis?',
    answer: 'Ya, Anda bisa memperpanjang dengan memesan kembali. Kami juga sering memberikan diskon khusus untuk pelanggan yang memperpanjang. Tim kami akan mengingatkan Anda sebelum masa aktif berakhir.',
    category: 'renewal'
  },
  {
    question: 'Bagaimana dengan paket tim? Apakah setiap anggota dapat akses pribadi?',
    answer: 'Ya, setiap anggota tim mendapat invite pribadi ke email mereka masing-masing. Tidak ada sharing password atau account. Setiap orang memiliki akses penuh dan pribadi ke ChatGPT Plus.',
    category: 'team'
  },
  {
    question: 'Apakah data saya aman dan terlindungi?',
    answer: 'Sangat aman. Kami tidak menyimpan data sensitif dan menggunakan enkripsi tingkat bank untuk semua transaksi. Kebijakan privasi kami sangat ketat dan kami mematuhi standar keamanan internasional.',
    category: 'security'
  },
  {
    question: 'Bisakah saya menggunakan untuk keperluan komersial?',
    answer: 'Ya, akses ChatGPT Plus yang Anda dapatkan sama persis dengan berlangganan langsung dari OpenAI. Anda bisa menggunakannya untuk keperluan personal maupun komersial tanpa batasan.',
    category: 'usage'
  }
];

const FAQSection: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'legal':
        return <Shield className="h-4 w-4 text-green-500" />;
      case 'guarantee':
        return <CheckCircle className="h-4 w-4 text-blue-500" />;
      default:
        return <HelpCircle className="h-4 w-4 text-gray-500" />;
    }
  };

  return (
    <section id="faq" className="py-12 bg-gradient-to-br from-gray-50 to-blue-50 relative">
      <div className="absolute inset-0 bg-[linear-gradient(rgba(59,130,246,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.02)_1px,transparent_1px)] bg-[size:50px_50px]"></div>
      
      <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-600 px-4 py-2 rounded-full text-sm font-semibold mb-4">
            <HelpCircle className="h-4 w-4" />
            <span>FAQ</span>
          </div>
          
          <h2 className="text-2xl md:text-3xl font-black text-gray-900 mb-4">
            Pertanyaan yang <span className="text-blue-600">Sering Diajukan</span>
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Jawaban untuk pertanyaan umum tentang layanan kami
          </p>
        </div>
        
        <div className="space-y-3">
          {faqs.slice(0, 4).map((faq, index) => (
            <div key={index} className="group">
              <div className={`bg-white rounded-xl shadow-sm border transition-all duration-300 overflow-hidden ${
                openIndex === index 
                  ? 'border-blue-200 shadow-lg' 
                  : 'border-gray-200 hover:border-blue-200 hover:shadow-lg'
              }`}>
                <button
                  onClick={() => toggleFAQ(index)}
                  className="w-full px-4 py-3 text-left flex justify-between items-center hover:bg-blue-50/50 focus:outline-none focus:bg-blue-50/50 transition-colors"
                >
                  <div className="flex items-start space-x-3 pr-3">
                    {getCategoryIcon(faq.category)}
                    <span className="font-bold text-gray-900 text-sm">{faq.question}</span>
                  </div>
                  <div className={`flex-shrink-0 transition-transform duration-300 ${
                    openIndex === index ? 'rotate-180' : ''
                  }`}>
                    {openIndex === index ? (
                      <ChevronUp className="h-5 w-5 text-blue-600" />
                    ) : (
                      <ChevronDown className="h-5 w-5 text-gray-400 group-hover:text-blue-600" />
                    )}
                  </div>
                </button>
                
                <div className={`transition-all duration-300 ${
                  openIndex === index 
                    ? 'max-h-40 opacity-100' 
                    : 'max-h-0 opacity-0'
                }`}>
                  <div className="px-4 pb-3">
                    <div className="h-px bg-gradient-to-r from-blue-200 to-indigo-200 mb-3"></div>
                    <p className="text-gray-700 leading-relaxed text-sm">{faq.answer}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Contact CTA */}
        <div className="mt-12 text-center">
          <div className="bg-white rounded-2xl p-6 shadow-md border border-gray-200">
            <div className="bg-gradient-to-br from-blue-500 to-indigo-600 w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-4 shadow-md">
              <HelpCircle className="h-6 w-6 text-white" />
            </div>
            <h3 className="text-xl font-black text-gray-900 mb-3">
              Masih ada pertanyaan?
            </h3>
            <p className="text-gray-600 mb-4 text-sm">
              Tim support kami siap membantu Anda 24/7
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="mailto:support@chatgptplus-legal.com"
                className="inline-flex items-center justify-center px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg hover:from-blue-500 hover:to-indigo-500 transition-all duration-300 font-semibold text-sm shadow-md"
              >
                Email Support
              </a>
              <a
                href="https://wa.me/6281234567890"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:from-green-500 hover:to-emerald-500 transition-all duration-300 font-semibold text-sm shadow-md"
              >
                WhatsApp
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FAQSection;
