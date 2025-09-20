"use client"

import type React from "react"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { useOrder } from "../contexts/OrderContext"
import { apiService } from "../services/apiService"
import { Mail, User, Phone, Loader2, AlertCircle } from "lucide-react"

const OrderForm: React.FC = () => {
  const router = useRouter()
  const { state, dispatch } = useOrder()
  const [formData, setFormData] = useState({
    customer_email: "",
    full_name: "",
    phone_number: "",
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  const validatePhone = (phone: string): boolean => {
    if (!phone) return true // Optional field
    const phoneRegex = /^(\+62|62|0)[0-9]{8,12}$/
    return phoneRegex.test(phone)
  }

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))

    // Real-time validation
    const newErrors = { ...errors }

    if (field === "customer_email") {
      if (!value) {
        newErrors[field] = "Email wajib diisi"
      } else if (!validateEmail(value)) {
        newErrors[field] = "Format email tidak valid"
      } else {
        delete newErrors[field]
      }
    }

    if (field === "phone_number") {
      if (value && !validatePhone(value)) {
        newErrors[field] = "Format nomor telepon tidak valid (contoh: +6281234567890)"
      } else {
        delete newErrors[field]
      }
    }

    setErrors(newErrors)
  }

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.customer_email) {
      newErrors.customer_email = "Email wajib diisi"
    } else if (!validateEmail(formData.customer_email)) {
      newErrors.customer_email = "Format email tidak valid"
    }

    if (formData.phone_number && !validatePhone(formData.phone_number)) {
      newErrors.phone_number = "Format nomor telepon tidak valid"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validateForm() || !state.selectedPackage) return

    setIsSubmitting(true)
    dispatch({ type: "SET_ERROR", payload: null })

    try {
      const orderData = {
        ...formData,
        package_id: state.selectedPackage.id,
      }

      const response = await apiService.createOrder(orderData)

      dispatch({ type: "SET_CURRENT_ORDER", payload: response })
      dispatch({ type: "UPDATE_ORDER_DATA", payload: orderData })

      router.push(`/confirmation?order_id=${response.order_id}`)
    } catch (error) {
      dispatch({
        type: "SET_ERROR",
        payload: error instanceof Error ? error.message : "Terjadi kesalahan sistem",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Informasi Pemesanan</h2>

      {state.error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-start space-x-3">
          <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-red-800 font-medium">Terjadi Kesalahan</p>
            <p className="text-red-700 text-sm">{state.error}</p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Email Field */}
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
            Email Address <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="email"
              id="email"
              value={formData.customer_email}
              onChange={(e) => handleInputChange("customer_email", e.target.value)}
              className={`w-full pl-10 pr-3 py-3 border rounded-lg focus:outline-none focus:ring-2 transition-colors ${
                errors.customer_email
                  ? "border-red-300 focus:ring-red-500 focus:border-red-500"
                  : "border-gray-300 focus:ring-blue-500 focus:border-blue-500"
              }`}
              placeholder="your@email.com"
              disabled={isSubmitting}
            />
          </div>
          {errors.customer_email && <p className="mt-1 text-sm text-red-600">{errors.customer_email}</p>}
          <p className="mt-1 text-sm text-gray-500">Undangan ChatGPT Plus akan dikirim ke email ini</p>
        </div>

        {/* Full Name Field */}
        <div>
          <label htmlFor="fullname" className="block text-sm font-medium text-gray-700 mb-2">
            Nama Lengkap (Opsional)
          </label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              id="fullname"
              value={formData.full_name}
              onChange={(e) => handleInputChange("full_name", e.target.value)}
              className="w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              placeholder="Nama Lengkap"
              disabled={isSubmitting}
            />
          </div>
        </div>

        {/* Phone Field */}
        <div>
          <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
            Nomor Telepon (Opsional)
          </label>
          <div className="relative">
            <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="tel"
              id="phone"
              value={formData.phone_number}
              onChange={(e) => handleInputChange("phone_number", e.target.value)}
              className={`w-full pl-10 pr-3 py-3 border rounded-lg focus:outline-none focus:ring-2 transition-colors ${
                errors.phone_number
                  ? "border-red-300 focus:ring-red-500 focus:border-red-500"
                  : "border-gray-300 focus:ring-blue-500 focus:border-blue-500"
              }`}
              placeholder="+6281234567890"
              disabled={isSubmitting}
            />
          </div>
          {errors.phone_number && <p className="mt-1 text-sm text-red-600">{errors.phone_number}</p>}
          <p className="mt-1 text-sm text-gray-500">Untuk notifikasi dan support WhatsApp</p>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isSubmitting || Object.keys(errors).length > 0 || !formData.customer_email}
          className="w-full bg-blue-600 text-white py-4 px-6 rounded-lg font-semibold text-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              <span>Memproses...</span>
            </>
          ) : (
            <span>Lanjutkan Pembayaran</span>
          )}
        </button>
      </form>
    </div>
  )
}

export default OrderForm
