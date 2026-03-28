import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import toast from 'react-hot-toast'
import { Upload, FileText, Loader2, AlertCircle } from 'lucide-react'
import { extractInvoice } from '../hooks/useApi'
import { ExtractionResult } from '../types/invoice'

interface Props {
  onResult: (data: ExtractionResult, filename: string) => void
}

const ACCEPTED = {
  'application/pdf': ['.pdf'],
  'image/jpeg': ['.jpg', '.jpeg'],
  'image/png': ['.png'],
  'image/bmp': ['.bmp'],
  'image/tiff': ['.tiff'],
}

export default function UploadZone({ onResult }: Props) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const processFile = useCallback(
    async (file: File) => {
      setLoading(true)
      setError(null)
      const toastId = toast.loading(`Processing "${file.name}"… this may take 20–60s`)

      try {
        const result = await extractInvoice(file)
        toast.success('Invoice extracted successfully!', { id: toastId })
        onResult(result, file.name)
      } catch (err: any) {
        const msg =
          err?.response?.data?.detail || err?.message || 'Extraction failed'
        setError(msg)
        toast.error(msg, { id: toastId })
      } finally {
        setLoading(false)
      }
    },
    [onResult]
  )

  const onDrop = useCallback(
    (accepted: File[]) => {
      if (accepted.length > 0) processFile(accepted[0])
    },
    [processFile]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED,
    maxFiles: 1,
    disabled: loading,
  })

  return (
    <div className="flex flex-col items-center gap-6 mt-6">
      {/* Hero text */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">
          Extract Invoice Data Instantly
        </h2>
        <p className="text-gray-500 max-w-md">
          Drop any invoice — PDF or image — and our OCR pipeline will pull out
          every field automatically.
        </p>
      </div>

      {/* Drop zone */}
      <div
        {...getRootProps()}
        className={`
          w-full max-w-2xl border-2 border-dashed rounded-2xl p-14 text-center
          cursor-pointer transition-all duration-200 select-none
          ${loading ? 'opacity-60 cursor-not-allowed' : ''}
          ${
            isDragActive
              ? 'border-blue-500 bg-blue-50 scale-[1.01]'
              : 'border-gray-300 bg-white hover:border-blue-400 hover:bg-blue-50'
          }
        `}
      >
        <input {...getInputProps()} />

        {loading ? (
          <div className="flex flex-col items-center gap-3 text-blue-600">
            <Loader2 size={48} className="animate-spin" />
            <p className="font-semibold text-lg">Running OCR pipeline…</p>
            <p className="text-sm text-gray-500">
              Large PDFs may take up to a minute
            </p>
          </div>
        ) : isDragActive ? (
          <div className="flex flex-col items-center gap-3 text-blue-600">
            <Upload size={48} />
            <p className="font-semibold text-lg">Drop it here!</p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-3 text-gray-400">
            <FileText size={48} />
            <p className="font-semibold text-lg text-gray-600">
              Drag &amp; drop your invoice here
            </p>
            <p className="text-sm">or click to browse files</p>
            <p className="text-xs mt-1 text-gray-400">
              PDF, JPG, PNG, BMP, TIFF · max 50 MB
            </p>
          </div>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-start gap-3 bg-red-50 border border-red-200 rounded-xl px-5 py-4 w-full max-w-2xl">
          <AlertCircle size={20} className="text-red-500 mt-0.5 shrink-0" />
          <div>
            <p className="font-semibold text-red-700 text-sm">Extraction failed</p>
            <p className="text-red-600 text-sm mt-0.5">{error}</p>
            <p className="text-xs text-gray-500 mt-1">
              Make sure the backend is running at <code>localhost:8000</code>
            </p>
          </div>
        </div>
      )}

      {/* Tips */}
      <div className="grid grid-cols-3 gap-4 w-full max-w-2xl text-center text-sm">
        {[
          { icon: '📄', label: 'PDF Invoices', desc: 'Multi-page supported' },
          { icon: '🖼️', label: 'Image Files', desc: 'JPG, PNG, BMP, TIFF' },
          { icon: '📊', label: 'Structured Output', desc: 'JSON & CSV export' },
        ].map((tip) => (
          <div
            key={tip.label}
            className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm"
          >
            <div className="text-2xl mb-1">{tip.icon}</div>
            <div className="font-medium text-gray-700">{tip.label}</div>
            <div className="text-gray-400 text-xs">{tip.desc}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
