import { useState } from 'react'
import { Toaster } from 'react-hot-toast'
import UploadZone from './components/UploadZone'
import ResultsPanel from './components/ResultsPanel'
import Header from './components/Header'
import { ExtractionResult } from './types/invoice'

export default function App() {
  const [result, setResult] = useState<ExtractionResult | null>(null)
  const [uploadedFilename, setUploadedFilename] = useState<string>('')

  const handleResult = (data: ExtractionResult, filename: string) => {
    setResult(data)
    setUploadedFilename(filename)
  }

  const handleReset = () => {
    setResult(null)
    setUploadedFilename('')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Toaster position="top-right" />
      <Header />
      <main className="max-w-5xl mx-auto px-4 py-10">
        {!result ? (
          <UploadZone onResult={handleResult} />
        ) : (
          <ResultsPanel
            result={result}
            filename={uploadedFilename}
            onReset={handleReset}
          />
        )}
      </main>
      <footer className="text-center text-xs text-gray-400 py-6">
        OCR Invoice Extractor · Harsmitha K &amp; Jahnavi K L · TechTheos Internship 2026
      </footer>
    </div>
  )
}
