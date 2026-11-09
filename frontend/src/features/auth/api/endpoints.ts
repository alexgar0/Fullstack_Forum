import { api, requireData, requireSuccess } from '../../../api/openapi'
import type { RegisterDTO, UserDTO } from './dto'

export async function login(username: string, password: string) {
  const result = await api.POST('/users/login', {
    credentials: 'same-origin',
    body: { username, password, scope: '' },
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  requireSuccess(result)
  return result.data
}

export async function register(
  username: string,
  email: string,
  password: string,
  password_check: string,
) {
  if (password !== password_check) {
    throw new Error("Passwords don't match")
  }

  const body: RegisterDTO = {
    username: username,
    email: email,
    password: password,
  }
  return requireData(await api.POST('/users/register', { body, credentials: 'same-origin' }))
}

export async function me(): Promise<UserDTO> {
  return requireData(await api.GET('/users/me', { credentials: 'same-origin' }))
}

export async function logout() {
  requireSuccess(await api.POST('/users/logout', { credentials: 'same-origin' }))
}
