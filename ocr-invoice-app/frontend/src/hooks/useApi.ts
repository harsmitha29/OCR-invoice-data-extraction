import axios from 'axios'
import { ExtractionResult } from '../types/invoice'

const API_BASE = '/api'

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 120000, // 2 minutes for OCR processing
})

export async function extractInvoice(file: File): Promise<ExtractionResult> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post<ExtractionResult>('/extract', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

  return response.data
}

export function getDownloadUrl(format: 'json' | 'csv', filename: string): string {
  const stem = filename.replace(/\.[^.]+$/, '')
  return `${API_BASE}/download/${format}/${stem}`
}

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await api.get('/health')
    return res.data.status === 'healthy'
  } catch {
    return false
  }
}
