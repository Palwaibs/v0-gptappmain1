"use client"

import type React from "react"
import { useRouter } from "next/navigation"
import { useOrder } from "../contexts/OrderContext"
import OrderForm from "../components/OrderForm"
import OrderSummary from "../components/OrderSummary"
import { ArrowLeft, Shield, Clock, CheckCircle } from "lucide-react"

const OrderPage: React.FC = () => {
  const router = useRouter()
  const { state } = useOrder()

  if (!state.selectedPackage) {
    router.push("/")
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => router.push("/")}
            className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors mb-4"
          >
            <ArrowLeft className="h-5 w-5" />
            <span>Kembali ke Paket</span>
          </button>

          <h1 className="text-3xl font-bold text-gray-900">Checkout</h1>
          <p className="text-gray-600 mt-2">Lengkapi data Anda untuk melanjutkan pemesanan</p>
        </div>

        {/* Trust Indicators */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center space-x-3">
              <Shield className="h-6 w-6 text-blue-600" />
              <div>
                <p className="font-medium text-blue-900">100% Aman</p>
                <p className="text-sm text-blue-700">Data dilindungi SSL</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Clock className="h-6 w-6 text-blue-600" />
              <div>
                <p className="font-medium text-blue-900">Proses Cepat</p>
                <p className="text-sm text-blue-700">5-30 menit setelah bayar</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <CheckCircle className="h-6 w-6 text-blue-600" />
              <div>
                <p className="font-medium text-blue-900">Garansi 30 Hari</p>
                <p className="text-sm text-blue-700">Uang kembali jika tidak puas</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Order Form */}
          <div className="lg:col-span-2">
            <OrderForm />
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <OrderSummary />
          </div>
        </div>
      </div>
    </div>
  )
}

export default OrderPage
