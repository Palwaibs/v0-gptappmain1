"use client"

import type React from "react"
import { useRouter } from "next/navigation"
import { useOrder, type Package } from "../contexts/OrderContext"
import PackageCard from "../components/PackageCard"
import FAQSection from "../components/FAQSection"
import TestimonialSection from "../components/TestimonialSection"
import { CheckCircle, Zap, Shield, Crown, TrendingUp, Heart, MessageCircle } from "lucide-react"

const packages: Package[] = [
  {
    id: "chatgpt_plus_1_month",
    name: "Individual Plan",
    price: 25000,
    originalPrice: 300000,
    duration: "1 Bulan",
    features: ["Akses ChatGPT Plus penuh", "Invite ke email pribadi", "Garansi 7 hari", "Support 24/7"],
    buttonText: "Pesan Sekarang",
    popular: true,
  },
  {
    id: "team_package",
    name: "Team Plan",
    price: 95000,
    originalPrice: 1500000,
    duration: "1 Bulan",
    features: ["Untuk 5 orang", "Email pribadi masing-masing", "Garansi 7 hari", "Support prioritas"],
    buttonText: "Pesan Tim",
  },
]

const LandingPage: React.FC = () => {
  const router = useRouter()
  const { dispatch } = useOrder()

  const handleSelectPackage = (pkg: Package) => {
    dispatch({ type: "SET_SELECTED_PACKAGE", payload: pkg })
    router.push("/order")
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section - Simplified */}
      <section className="relative bg-gradient-to-br from-slate-900 to-blue-900 text-white py-12 md:py-20">
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:20px_20px]"></div>

        <div className="relative max-w-4xl mx-auto px-4 sm:px-6 text-center">
          {/* Trust Badge */}
          <div className="inline-flex items-center space-x-2 bg-green-500/20 border border-green-500/30 rounded-full px-3 py-1.5 mb-6 text-sm">
            <Shield className="h-4 w-4 text-green-400" />
            <span className="font-semibold text-green-300">100% LEGAL & AMAN</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-3xl md:text-5xl font-black mb-4 leading-tight">
            ChatGPT Plus Legal
            <span className="block text-blue-400 mt-2">Hemat 92% - Mulai 25k</span>
          </h1>

          {/* Simple Description */}
          <p className="text-lg md:text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Akses ChatGPT Plus resmi via invite email pribadi.
            <strong className="text-green-400"> Bukan sharing account</strong>, dengan garansi penuh.
          </p>

          {/* Key Benefits - Simplified */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
              <Shield className="h-5 w-5 text-green-400 mx-auto mb-1.5" />
              <p className="text-sm font-semibold">100% Legal</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
              <TrendingUp className="h-5 w-5 text-blue-400 mx-auto mb-1.5" />
              <p className="text-sm font-semibold">Hemat 92%</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
              <Heart className="h-5 w-5 text-red-400 mx-auto mb-1.5" />
              <p className="text-sm font-semibold">Garansi 7 Hari</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
              <Zap className="h-5 w-5 text-yellow-400 mx-auto mb-1.5" />
              <p className="text-sm font-semibold">Proses Cepat</p>
            </div>
          </div>

          {/* CTA */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-6">
            <button
              onClick={() => handleSelectPackage(packages[0])}
              className="w-full sm:w-auto bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-lg font-bold text-lg hover:from-blue-500 hover:to-indigo-500 transition-all duration-300 shadow-lg"
            >
              Pesan Sekarang - Rp 25k
            </button>
            <a
              href="https://wa.me/6281234567890"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto flex items-center justify-center space-x-2 bg-green-600 text-white px-8 py-4 rounded-lg hover:bg-green-700 transition-colors font-semibold text-lg"
            >
              <MessageCircle className="h-4 w-4" />
              <span>Tanya via WhatsApp</span>
            </a>
          </div>

          {/* Social Proof */}
          <div className="flex items-center justify-center space-x-3 text-sm text-gray-300">
            <div className="flex -space-x-1">
              <div className="w-5 h-5 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-full border-2 border-slate-800"></div>
              <div className="w-5 h-5 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full border-2 border-slate-800"></div>
              <div className="w-5 h-5 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full border-2 border-slate-800"></div>
            </div>
            <span className="text-sm">2,000+ pengguna puas</span>
          </div>
        </div>
      </section>

      {/* GPT Free vs Plus Comparison */}
      <section className="py-12 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-8">
            <h2 className="text-2xl md:text-3xl font-black text-gray-900 mb-3">
              Mengapa Upgrade ke <span className="text-blue-600">ChatGPT Plus?</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {/* GPT Free */}
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="text-center mb-4">
                <div className="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center mx-auto mb-3">
                  <span className="text-gray-600 font-bold">FREE</span>
                </div>
                <h3 className="text-lg font-bold text-gray-900">ChatGPT Free</h3>
              </div>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center space-x-2">
                  <span className="w-4 h-4 bg-red-100 rounded-full flex items-center justify-center">
                    <span className="text-red-600 text-xs">✗</span>
                  </span>
                  <span>Akses terbatas saat peak hours</span>
                </li>
                <li className="flex items-center space-x-2">
                  <span className="w-4 h-4 bg-red-100 rounded-full flex items-center justify-center">
                    <span className="text-red-600 text-xs">✗</span>
                  </span>
                  <span>Model GPT-3.5 saja</span>
                </li>
                <li className="flex items-center space-x-2">
                  <span className="w-4 h-4 bg-red-100 rounded-full flex items-center justify-center">
                    <span className="text-red-600 text-xs">✗</span>
                  </span>
                  <span>Tidak ada akses GPT-4</span>
                </li>
                <li className="flex items-center space-x-2">
                  <span className="w-4 h-4 bg-red-100 rounded-full flex items-center justify-center">
                    <span className="text-red-600 text-xs">✗</span>
                  </span>
                  <span>Respon lebih lambat</span>
                </li>
              </ul>
            </div>

            {/* GPT Plus */}
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 shadow-sm border-2 border-blue-200">
              <div className="text-center mb-4">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center mx-auto mb-3">
                  <Crown className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-lg font-bold text-gray-900">ChatGPT Plus</h3>
                <div className="text-sm text-blue-600 font-semibold">Hanya 25k/bulan</div>
              </div>
              <ul className="space-y-2 text-sm text-gray-700">
                <li className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Akses prioritas tanpa antrian</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>GPT-4 model terbaru</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Respon 5x lebih cepat</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Fitur advanced & plugins</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Packages Section */}
      <section className="py-12 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-8">
            <h2 className="text-2xl md:text-3xl font-black text-gray-900 mb-3">
              Pilih <span className="text-blue-600">Paket Anda</span>
            </h2>
            <p className="text-gray-600">Hemat hingga 92% dari harga resmi</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-3xl mx-auto">
            {packages.map((pkg) => (
              <PackageCard key={pkg.id} package={pkg} onSelect={() => handleSelectPackage(pkg)} />
            ))}
          </div>
        </div>
      </section>

      {/* How It Works - Simplified */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-12">
            <h2 className="text-2xl md:text-3xl font-black text-gray-900 mb-3">
              Cara <span className="text-blue-600">Kerja</span>
            </h2>
            <p className="text-sm md:text-base text-gray-600">Proses mudah dalam 3 langkah</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="bg-blue-600 w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-3 text-white font-bold text-sm">
                1
              </div>
              <h3 className="font-bold text-gray-900 mb-2 text-sm">Pesan & Bayar</h3>
              <p className="text-sm text-gray-600">Pilih paket dan lakukan pembayaran</p>
            </div>
            <div className="text-center">
              <div className="bg-blue-600 w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-3 text-white font-bold text-sm">
                2
              </div>
              <h3 className="font-bold text-gray-900 mb-2 text-sm">Terima Invite</h3>
              <p className="text-sm text-gray-600">Invite resmi dikirim ke email Anda</p>
            </div>
            <div className="text-center">
              <div className="bg-blue-600 w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-3 text-white font-bold text-sm">
                3
              </div>
              <h3 className="font-bold text-gray-900 mb-2 text-sm">Nikmati Akses</h3>
              <p className="text-sm text-gray-600">Klik link dan mulai gunakan ChatGPT Plus</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <TestimonialSection />

      {/* FAQ */}
      <FAQSection />

      {/* Final CTA - Simple */}
      <section className="py-16 bg-gradient-to-br from-blue-600 to-indigo-700 text-white">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 text-center">
          <h2 className="text-2xl md:text-3xl font-black mb-3">Siap Menghemat 92%?</h2>
          <p className="text-base md:text-lg mb-6 text-blue-100">
            Bergabung dengan 2,000+ pengguna yang sudah merasakan manfaatnya
          </p>

          <div className="flex flex-col sm:flex-row gap-3 justify-center items-center mb-6">
            <button
              onClick={() => handleSelectPackage(packages[0])}
              className="w-full sm:w-auto bg-gradient-to-r from-orange-500 to-red-600 text-white px-6 py-3 rounded-lg font-bold text-base hover:from-orange-400 hover:to-red-500 transition-all duration-300 shadow-lg"
            >
              Pesan Sekarang - Rp 25k
            </button>

            <a
              href="https://wa.me/6281234567890"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto flex items-center justify-center space-x-2 bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors font-semibold text-base"
            >
              <MessageCircle className="h-5 w-5" />
              <span>Tanya via WhatsApp</span>
            </a>
          </div>

          <p className="text-sm text-blue-200">✅ Garansi 7 Hari • 🔒 100% Legal • ⚡ Proses Cepat</p>
        </div>
      </section>
    </div>
  )
}

export default LandingPage
