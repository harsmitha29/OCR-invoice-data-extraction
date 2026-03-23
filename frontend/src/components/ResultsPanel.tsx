import { useState } from 'react'
import {
  CheckCircle2,
  XCircle,
  RotateCcw,
  Download,
  ChevronDown,
  ChevronUp,
  FileJson,
  FileSpreadsheet,
} from 'lucide-react'
import { ExtractionResult } from '../types/invoice'
import { getDownloadUrl } from '../hooks/useApi'

interface Props {
  result: ExtractionResult
  filename: string
  onReset: () => void
}

function Field({ label, value }: { label: string; value: string | number }) {
  const display =
    value === '' || value === null || value === undefined ? (
      <span className="text-gray-400 italic">Not detected</span>
    ) : (
      <span className="text-gray-900 font-medium">{String(value)}</span>
    )

  return (
    <div className="flex flex-col gap-0.5">
      <span className="text-xs text-gray-500 uppercase tracking-wide font-semibold">
        {label}
      </span>
      {display}
    </div>
  )
}

function CurrencyField({ label, value }: { label: string; value: number }) {
  const formatted =
    value > 0
      ? `₹ ${value.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`
      : null

  return (
    <div className="flex flex-col gap-0.5">
      <span className="text-xs text-gray-500 uppercase tracking-wide font-semibold">
        {label}
      </span>
      {formatted ? (
        <span className="text-gray-900 font-semibold text-lg">{formatted}</span>
      ) : (
        <span className="text-gray-400 italic text-sm">Not detected</span>
      )}
    </div>
  )
}

export default function ResultsPanel({ result, filename, onReset }: Props) {
  const [showRaw, setShowRaw] = useState(false)
  const { data } = result
  const stem = filename.replace(/\.[^.]+$/, '')

  return (
    <div className="flex flex-col gap-6">
      {/* Top bar */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Extraction Results</h2>
          <p className="text-sm text-gray-500">{filename}</p>
        </div>
        <button
          onClick={onReset}
          className="flex items-center gap-2 text-sm bg-white border border-gray-200 rounded-lg px-4 py-2 hover:bg-gray-50 transition"
        >
          <RotateCcw size={15} />
          Upload another
        </button>
      </div>

      {/* Validation badge */}
      <div
        className={`flex items-center gap-3 rounded-xl px-5 py-3 border ${
          data.validation_passed
            ? 'bg-green-50 border-green-200'
            : 'bg-yellow-50 border-yellow-200'
        }`}
      >
        {data.validation_passed ? (
          <>
            <CheckCircle2 size={20} className="text-green-600 shrink-0" />
            <span className="text-green-800 font-medium text-sm">
              Validation passed — all required fields detected
            </span>
          </>
        ) : (
          <>
            <XCircle size={20} className="text-yellow-600 shrink-0" />
            <div>
              <span className="text-yellow-800 font-medium text-sm block">
                Some fields could not be detected
              </span>
              {data.validation_errors?.length > 0 && (
                <ul className="text-yellow-700 text-xs mt-0.5 list-disc list-inside">
                  {data.validation_errors.map((e, i) => (
                    <li key={i}>{e}</li>
                  ))}
                </ul>
              )}
            </div>
          </>
        )}
      </div>

      {/* Main fields */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 bg-gray-50">
          <h3 className="font-semibold text-gray-700 text-sm uppercase tracking-wide">
            Invoice Details
          </h3>
        </div>
        <div className="p-6 grid grid-cols-2 gap-6">
          <Field label="Invoice Number" value={data.invoice_number} />
          <Field label="Invoice Date" value={data.invoice_date} />
          <Field label="Vendor / Supplier" value={data.vendor?.name} />
          <Field label="Customer" value={data.customer?.name} />
        </div>
      </div>

      {/* Amounts */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 bg-gray-50">
          <h3 className="font-semibold text-gray-700 text-sm uppercase tracking-wide">
            Financial Summary
          </h3>
        </div>
        <div className="p-6 grid grid-cols-3 gap-6">
          <CurrencyField label="Subtotal" value={data.subtotal} />
          <CurrencyField label="Tax / GST" value={data.tax} />
          <div className="flex flex-col gap-0.5 col-span-1 bg-blue-50 rounded-xl px-4 py-3 border border-blue-100">
            <span className="text-xs text-blue-600 uppercase tracking-wide font-semibold">
              Total Amount
            </span>
            {data.total > 0 ? (
              <span className="text-blue-700 font-bold text-2xl">
                ₹{' '}
                {data.total.toLocaleString('en-IN', {
                  minimumFractionDigits: 2,
                })}
              </span>
            ) : (
              <span className="text-gray-400 italic text-sm">Not detected</span>
            )}
          </div>
        </div>
      </div>

      {/* Downloads */}
      <div className="flex items-center gap-3">
        <span className="text-sm text-gray-500 font-medium">Download as:</span>
        <a
          href={getDownloadUrl('json', filename)}
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-2 bg-white border border-gray-200 hover:border-blue-400 hover:text-blue-600 text-sm rounded-lg px-4 py-2 transition shadow-sm"
        >
          <FileJson size={16} />
          JSON
        </a>
        <a
          href={getDownloadUrl('csv', filename)}
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-2 bg-white border border-gray-200 hover:border-green-400 hover:text-green-600 text-sm rounded-lg px-4 py-2 transition shadow-sm"
        >
          <FileSpreadsheet size={16} />
          CSV
        </a>
      </div>

      {/* Raw text toggle */}
      {data.raw_text && (
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          <button
            onClick={() => setShowRaw(!showRaw)}
            className="w-full flex items-center justify-between px-6 py-4 text-sm font-medium text-gray-600 hover:bg-gray-50 transition"
          >
            <span>Raw OCR Text</span>
            {showRaw ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>
          {showRaw && (
            <pre className="px-6 pb-6 text-xs text-gray-600 whitespace-pre-wrap overflow-auto max-h-64 font-mono bg-gray-50 border-t border-gray-100">
              {data.raw_text}
            </pre>
          )}
        </div>
      )}
    </div>
  )
}
