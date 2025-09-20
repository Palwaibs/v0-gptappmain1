"use client"

import type React from "react"
import { useEffect, useState } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { useOrder } from "../contexts/OrderContext"
import { apiService } from "../services/apiService"
import DemoControls from "../components/DemoControls"
import { CheckCircle, Clock, XCircle, AlertCircle, Loader2, ArrowLeft, MessageCircle } from "lucide-react"

interface OrderStatus {
  order_id: string
  payment_status: "pending" | "paid" | "failed" | "expired"
  invitation_status: "pending" | "processing" | "sent" | "failed" | "manual_review_required"
  message: string
}

const ConfirmationPage: React.FC = () => {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { state, dispatch } = useOrder()
  const [orderStatus, setOrderStatus] = useState<OrderStatus | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null)
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const orderId = searchParams.get("order_id") || state.currentOrder?.order_id

  // Debug logging
  console.log("ConfirmationPage - orderId:", orderId)
  console.log("ConfirmationPage - searchParams:", Object.fromEntries(searchParams))
  console.log("ConfirmationPage - state.currentOrder:", state.currentOrder)

  useEffect(() => {
    if (!orderId) {
      console.log("No orderId found, redirecting to home")
      router.push("/")
      return
    }

    const fetchOrderStatus = async () => {
      try {
        const status = await apiService.getOrderStatus(orderId)
        setOrderStatus(status)
        setIsLoading(false)

        // Start polling if payment is pending or invitation is processing
        if (status.payment_status === "pending" || status.invitation_status === "processing") {
          const interval = setInterval(async () => {
            try {
              const updatedStatus = await apiService.getOrderStatus(orderId)
              setOrderStatus(updatedStatus)

              // Stop polling if payment failed/expired or invitation completed
              if (
                updatedStatus.payment_status === "failed" ||
                updatedStatus.payment_status === "expired" ||
                updatedStatus.invitation_status === "sent" ||
                updatedStatus.invitation_status === "failed"
              ) {
                clearInterval(interval)
                setPollingInterval(null)
              }
            } catch (error) {
              console.error("Error polling order status:", error)
            }
          }, 5000) // Poll every 5 seconds

          setPollingInterval(interval)
        }
      } catch (error) {
        dispatch({
          type: "SET_ERROR",
          payload: error instanceof Error ? error.message : "Tidak dapat memuat status order",
        })
        setIsLoading(false)
      }
    }

    fetchOrderStatus()

    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval)
      }
    }
  }, [orderId, router, dispatch, refreshTrigger])

  const handleRefresh = () => {
    setRefreshTrigger((prev) => prev + 1)
  }

  const getStatusIcon = () => {
    if (!orderStatus) return null

    switch (orderStatus.payment_status) {
      case "paid":
        switch (orderStatus.invitation_status) {
          case "sent":
            return <CheckCircle className="h-16 w-16 text-green-500" />
          case "processing":
            return <Loader2 className="h-16 w-16 text-blue-500 animate-spin" />
          case "failed":
          case "manual_review_required":
            return <AlertCircle className="h-16 w-16 text-yellow-500" />
          default:
            return <Clock className="h-16 w-16 text-blue-500" />
        }
      case "pending":
        return <Clock className="h-16 w-16 text-yellow-500" />
      case "failed":
      case "expired":
        return <XCircle className="h-16 w-16 text-red-500" />
      default:
        return <Clock className="h-16 w-16 text-gray-500" />
    }
  }

  const getStatusMessage = () => {
    if (!orderStatus) return ""

    switch (orderStatus.payment_status) {
      case "paid":
        switch (orderStatus.invitation_status) {
          case "sent":
            return {
              title: "Pembayaran Berhasil & Undangan Terkirim!",
              description: "Undangan ChatGPT Plus telah dikirim ke email Anda. Silakan cek inbox dan spam folder.",
              type: "success",
            }
          case "processing":
            return {
              title: "Pembayaran Berhasil!",
              description: "Undangan sedang diproses dan akan dikirim dalam 5-30 menit.",
              type: "processing",
            }
          case "failed":
          case "manual_review_required":
            return {
              title: "Pembayaran Berhasil",
              description: "Ada kendala teknis dalam pengiriman undangan. Tim support akan menghubungi Anda segera.",
              type: "warning",
            }
          default:
            return {
              title: "Pembayaran Berhasil!",
              description: "Proses undangan akan segera dimulai.",
              type: "success",
            }
        }
      case "pending":
        return {
          title: "Menunggu Pembayaran",
          description: "Silakan selesaikan pembayaran sesuai instruksi yang diberikan.",
          type: "pending",
        }
      case "failed":
        return {
          title: "Pembayaran Gagal",
          description: "Pembayaran tidak dapat diproses. Silakan coba lagi atau hubungi support.",
          type: "error",
        }
      case "expired":
        return {
          title: "Pembayaran Kedaluwarsa",
          description: "Waktu pembayaran telah habis. Silakan buat pesanan baru.",
          type: "error",
        }
      default:
        return {
          title: "Memproses...",
          description: "Sedang memproses status pesanan Anda.",
          type: "pending",
        }
    }
  }

  const getEstimatedTime = () => {
    if (!orderStatus) return ""

    if (orderStatus.payment_status === "paid") {
      switch (orderStatus.invitation_status) {
        case "processing":
          return "Estimasi: 5-30 menit"
        case "sent":
          return "Selesai"
        default:
          return "Sedang diproses"
      }
    }

    return ""
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-12 w-12 text-blue-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Memuat status pesanan...</p>
        </div>
      </div>
    )
  }

  if (!orderStatus) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md">
          <XCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Pesanan Tidak Ditemukan</h1>
          <p className="text-gray-600 mb-6">Order ID tidak valid atau tidak ditemukan dalam sistem.</p>
          <button
            onClick={() => router.push("/")}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Kembali ke Beranda
          </button>
        </div>
      </div>
    )
  }

  const statusMessage = getStatusMessage()

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => router.push("/")}
            className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors mb-4"
          >
            <ArrowLeft className="h-5 w-5" />
            <span>Kembali ke Beranda</span>
          </button>
        </div>

        {/* Status Card */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center mb-8">
          <div className="mb-6">{getStatusIcon()}</div>

          <h1 className="text-3xl font-bold text-gray-900 mb-4">{statusMessage.title}</h1>

          <p className="text-lg text-gray-600 mb-6 max-w-2xl mx-auto">{statusMessage.description}</p>

          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <p className="text-gray-500">Order ID</p>
                <p className="font-medium text-gray-900">{orderStatus.order_id}</p>
              </div>
              <div>
                <p className="text-gray-500">Status Pembayaran</p>
                <p className="font-medium capitalize text-gray-900">
                  {orderStatus.payment_status === "paid"
                    ? "Berhasil"
                    : orderStatus.payment_status === "pending"
                      ? "Menunggu"
                      : orderStatus.payment_status === "failed"
                        ? "Gagal"
                        : "Kedaluwarsa"}
                </p>
              </div>
              <div>
                <p className="text-gray-500">Status Undangan</p>
                <p className="font-medium capitalize text-gray-900">
                  {orderStatus.invitation_status === "sent"
                    ? "Terkirim"
                    : orderStatus.invitation_status === "processing"
                      ? "Diproses"
                      : orderStatus.invitation_status === "failed"
                        ? "Gagal"
                        : "Menunggu"}
                </p>
              </div>
            </div>
          </div>

          {getEstimatedTime() && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <p className="text-blue-800 font-medium">{getEstimatedTime()}</p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            {(orderStatus.payment_status === "failed" || orderStatus.payment_status === "expired") && (
              <button
                onClick={() => router.push("/order")}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Coba Lagi
              </button>
            )}

            <a
              href="https://wa.me/6281234567890"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center space-x-2 bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors"
            >
              <MessageCircle className="h-5 w-5" />
              <span>Hubungi Support</span>
            </a>
          </div>
        </div>

        {/* Additional Info */}
        {orderStatus.payment_status === "paid" && orderStatus.invitation_status === "sent" && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <h3 className="font-semibold text-green-800 mb-3">Langkah Selanjutnya:</h3>
            <ol className="list-decimal list-inside space-y-2 text-green-700">
              <li>Cek email Anda (termasuk folder spam/junk)</li>
              <li>Klik link undangan ChatGPT Team yang dikirim</li>
              <li>Ikuti instruksi untuk bergabung dengan tim</li>
              <li>Mulai menggunakan ChatGPT Plus dengan akses premium</li>
            </ol>
          </div>
        )}
      </div>

      <DemoControls orderId={orderId} onRefresh={handleRefresh} />
    </div>
  )
}

export default ConfirmationPage
