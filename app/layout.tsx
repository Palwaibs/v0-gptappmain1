import type React from "react"
import type { Metadata } from "next"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"
import { OrderProvider } from "../src/contexts/OrderContext"
import Header from "../src/components/Header"
import Footer from "../src/components/Footer"
import { Suspense } from "react"

export const metadata: Metadata = {
  title: "Akses GPT Murah - ChatGPT Plus Indonesia",
  description: "Dapatkan akses ChatGPT Plus dengan harga terjangkau di Indonesia",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <head>
        <style>{`
html {
  font-family: ${GeistSans.style.fontFamily};
  --font-sans: ${GeistSans.variable};
  --font-mono: ${GeistMono.variable};
}
        `}</style>
      </head>
      <body>
        <Suspense fallback={<div>Loading...</div>}>
          <OrderProvider>
            <div className="min-h-screen bg-gray-50 flex flex-col">
              <Header />
              <main className="flex-1">{children}</main>
              <Footer />
            </div>
          </OrderProvider>
        </Suspense>
        <Analytics />
      </body>
    </html>
  )
}
