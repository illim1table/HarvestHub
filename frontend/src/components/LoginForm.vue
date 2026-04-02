<template>
  <form class="login-form" @submit.prevent="handleSubmit">
    <input v-model="email" type="email" placeholder="邮箱" required />
    <input v-model="password" type="password" placeholder="密码" minlength="6" required />
    <button type="submit" :disabled="loading">{{ loading ? '登录中...' : '登录' }}</button>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { login } from '../api/index.js'

const emit = defineEmits(['login-success'])

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await login({ email: email.value, password: password.value })
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('username', data.username)
    localStorage.setItem('role', data.role)
    emit('login-success', { username: data.username, role: data.role })
    email.value = ''
    password.value = ''
  } catch (err) {
    error.value = err?.response?.data?.detail || '登录失败，请稍后再试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-form {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
}

.login-form input {
  height: 36px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  padding: 0 10px;
  min-width: 180px;
}

.login-form button {
  height: 36px;
  border: none;
  border-radius: 6px;
  background: #2e7d32;
  color: #fff;
  padding: 0 14px;
  cursor: pointer;
}

.login-form button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error {
  width: 100%;
  text-align: center;
  color: #c62828;
  font-size: 13px;
}
</style>
