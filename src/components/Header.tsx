"use client"

import React from "react"
import Link from "next/link"
import { Shield, TestTube, Menu, X } from "lucide-react"

const Header: React.FC = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false)

  const USE_MOCK_API = true // Force demo mode for preview

  return (
    <header className="bg-slate-900/95 backdrop-blur-md border-b border-slate-700/50 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-14">
          <Link href="/" className="flex items-center space-x-3 group">
            <div className="p-1.5 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg group-hover:from-blue-400 group-hover:to-indigo-500 transition-all duration-300 shadow-md">
              <Shield className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-black text-white">ChatGPT Plus Legal</h1>
              <p className="text-xs text-blue-400 font-medium leading-none">
                Hemat 70% - Garansi Penuh {USE_MOCK_API && "(Demo)"}
              </p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-4">
            {USE_MOCK_API && (
              <div className="flex items-center space-x-1 bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded-full text-xs border border-yellow-500/30">
                <TestTube className="h-4 w-4" />
                <span>Demo Mode</span>
              </div>
            )}
            <a href="#faq" className="text-gray-300 hover:text-blue-400 transition-colors font-medium text-sm">
              FAQ
            </a>
            <a href="#contact" className="text-gray-300 hover:text-blue-400 transition-colors font-medium text-sm">
              Kontak
            </a>
            <Link
              href="/order"
              className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-3 py-1.5 rounded-lg hover:from-blue-500 hover:to-indigo-500 transition-all duration-300 font-semibold text-sm"
            >
              Pesan Sekarang
            </Link>
          </nav>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-slate-800 transition-colors"
          >
            {isMobileMenuOpen ? <X className="h-5 w-5 text-gray-300" /> : <Menu className="h-5 w-5 text-gray-300" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-slate-700/50 py-2">
            <div className="flex flex-col space-y-2">
              {USE_MOCK_API && (
                <div className="flex items-center justify-center space-x-1 bg-yellow-500/20 text-yellow-400 px-2 py-0.5 rounded-full text-xs border border-yellow-500/30 w-fit mx-auto">
                  <TestTube className="h-3 w-3" />
                  <span>Demo Mode</span>
                </div>
              )}
              <a
                href="#faq"
                className="text-gray-300 hover:text-blue-400 transition-colors font-medium text-sm text-center py-1"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                FAQ
              </a>
              <a
                href="#contact"
                className="text-gray-300 hover:text-blue-400 transition-colors font-medium text-sm text-center py-1"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Kontak
              </a>
              <Link
                href="/order"
                className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-3 py-1.5 rounded-lg hover:from-blue-500 hover:to-indigo-500 transition-all duration-300 font-semibold text-sm text-center mx-4"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Pesan Sekarang
              </Link>
            </div>
          </div>
        )}
      </div>
    </header>
  )
}

export default Header
