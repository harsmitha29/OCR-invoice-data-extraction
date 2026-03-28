export interface VendorInfo {
  name: string
}

export interface CustomerInfo {
  name: string
}

export interface InvoiceData {
  invoice_number: string
  invoice_date: string
  vendor: VendorInfo
  customer: CustomerInfo
  subtotal: number
  tax: number
  total: number
  validation_passed: boolean
  validation_errors: string[]
  raw_text?: string
}

export interface ExtractionResult {
  success: boolean
  filename: string
  data: InvoiceData
}

export type UploadStatus = 'idle' | 'uploading' | 'success' | 'error'
