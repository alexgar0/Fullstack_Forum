import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  withCredentials: false, // включишь, если нужны куки
})

// перехватчик ошибок (по желанию)
http.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API error:', error)
    throw error
  }
)

export default http