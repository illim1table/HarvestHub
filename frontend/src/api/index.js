import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

export function getHealth() {
  return api.get('/health')
}

export function getProducts() {
  return api.get('/products')
}

export function getProduct(id) {
  return api.get(`/products/${id}`)
}

export default api
