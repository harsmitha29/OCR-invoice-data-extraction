import { FileText } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-5xl mx-auto px-4 py-4 flex items-center gap-3">
        <div className="bg-blue-600 text-white rounded-xl p-2">
          <FileText size={22} />
        </div>
        <div>
          <h1 className="text-xl font-bold text-gray-900 leading-tight">
            OCR Invoice Extractor
          </h1>
          <p className="text-xs text-gray-500">
            Upload an invoice PDF or image to extract structured data
          </p>
        </div>
      </div>
    </header>
  )
}
