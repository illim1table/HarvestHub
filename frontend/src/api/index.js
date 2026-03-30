import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export function getHealth() {
  return api.get('/health')
}

export function getCategories() {
  return api.get('/categories')
}

export function getProducts(params = {}) {
  return api.get('/products', { params })
}

export function getProduct(id) {
  return api.get(`/products/${id}`)
}

export function createProduct(payload) {
  return api.post('/products', payload)
}

export function login(payload) {
  return api.post('/auth/login', payload)
}

export default api
