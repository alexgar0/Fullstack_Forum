import createClient from 'openapi-fetch'
import type { paths } from './schema.generated'

export const api = createClient<paths>({
  baseUrl: import.meta.env.VITE_API_URL || '/api',
  credentials: 'include',
})

export class ApiError extends Error {
  readonly status: number
  readonly detail: string | undefined

  constructor(status: number, body: unknown) {
    const message =
      typeof body === 'object' &&
      body !== null &&
      'message' in body &&
      typeof body.message === 'string'
        ? body.message
        : 'Unexpected error'
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.detail =
      typeof body === 'object' &&
      body !== null &&
      'detail' in body &&
      typeof body.detail === 'string'
        ? body.detail
        : undefined
  }
}

export function requireSuccess(result: { error?: unknown; response: Response }): void {
  if (!result.response.ok) throw new ApiError(result.response.status, result.error)
}

export function requireData<T>(result: { data?: T; error?: unknown; response: Response }): T {
  requireSuccess(result)
  if (result.data === undefined) throw new Error('API returned an empty response')
  return result.data
}
