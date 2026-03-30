<template>
  <div id="app">
    <header class="header">
      <div class="header-inner">
        <div class="logo">
          <span class="logo-icon">🌾</span>
          <span class="logo-text">汇农亩场</span>
          <span class="logo-sub">农产品交易平台</span>
        </div>
        <nav class="nav">
          <a href="#">首页</a>
          <a href="#">分类</a>
          <a href="#">关于我们</a>
        </nav>
        <div class="user-status">
          <span v-if="currentUsername" class="user-badge">👤 {{ currentUsername }}</span>
          <span v-else class="user-badge guest">未登录</span>
        </div>
      </div>
    </header>

    <main class="main">
      <section class="hero">
        <h1>新鲜直达，产地直供</h1>
        <p>汇聚优质农产品，让每一口都充满自然的味道</p>
        <div class="health-badge" :class="healthStatus">
          <span class="dot"></span>
          {{ healthMessage }}
        </div>
        <div v-if="!currentUsername" class="login-section">
          <LoginForm @login-success="handleLoginSuccess" />
        </div>
      </section>

      <section class="products-section">
        <h2 class="section-title">🛒 精选农产品</h2>
        <PublishProductForm v-if="currentUsername" @created="refreshProductList" />
        <CartPanel
          :items="cartItems"
          :total-amount="cartTotalAmount"
          :submitting="orderSubmitting"
          :message="orderMessage"
          :error="orderError"
          @remove="removeCartItem"
          @submit="submitOrder"
        />
        <ProductList ref="productListRef" @add-to-cart="handleAddToCart" />
        <MyOrders v-if="currentUsername" ref="myOrdersRef" />
      </section>
    </main>

    <footer class="footer">
      <p>© 2024 汇农亩场 · 让农业更有价值</p>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { createOrder, getHealth } from './api/index.js'
import CartPanel from './components/CartPanel.vue'
import LoginForm from './components/LoginForm.vue'
import MyOrders from './components/MyOrders.vue'
import ProductList from './components/ProductList.vue'
import PublishProductForm from './components/PublishProductForm.vue'

const healthStatus = ref('unknown')
const healthMessage = ref('正在检测后端服务...')
const currentUsername = ref(localStorage.getItem('username') || '')
const productListRef = ref(null)
const myOrdersRef = ref(null)
const cartItems = ref([])
const orderSubmitting = ref(false)
const orderMessage = ref('')
const orderError = ref('')

function handleLoginSuccess(username) {
  currentUsername.value = username
  myOrdersRef.value?.loadOrders()
}

function refreshProductList() {
  productListRef.value?.refreshProducts()
}

function handleAddToCart({ product, quantity }) {
  orderMessage.value = ''
  orderError.value = ''
  const existing = cartItems.value.find((item) => item.product_id === product.id)
  if (existing) {
    existing.quantity += quantity
  } else {
    cartItems.value.push({
      product_id: product.id,
      product_name: product.name,
      price: Number(product.price),
      quantity,
    })
  }
}

function removeCartItem(productId) {
  cartItems.value = cartItems.value.filter((item) => item.product_id !== productId)
}

const cartTotalAmount = computed(() =>
  cartItems.value.reduce((sum, item) => sum + item.price * item.quantity, 0).toFixed(2),
)

async function submitOrder() {
  orderMessage.value = ''
  orderError.value = ''
  if (!localStorage.getItem('token')) {
    orderError.value = '请先登录后再下单'
    return
  }
  if (!cartItems.value.length) {
    orderError.value = '购物车为空，无法下单'
    return
  }
  orderSubmitting.value = true
  try {
    await createOrder({
      items: cartItems.value.map((item) => ({
        product_id: item.product_id,
        quantity: item.quantity,
      })),
    })
    orderMessage.value = '下单成功'
    cartItems.value = []
    productListRef.value?.refreshProducts()
    myOrdersRef.value?.loadOrders()
  } catch (err) {
    orderError.value = err?.response?.data?.detail || '下单失败，请稍后重试'
  } finally {
    orderSubmitting.value = false
  }
}

onMounted(async () => {
  try {
    const res = await getHealth()
    healthStatus.value = 'online'
    healthMessage.value = `后端服务在线 · ${res.data.message}`
  } catch {
    healthStatus.value = 'offline'
    healthMessage.value = '后端服务离线，请检查服务状态'
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: #f5f7f5;
  color: #333;
}

.header {
  background: linear-gradient(135deg, #2e7d32, #4caf50);
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  min-height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 8px 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
}

.logo-sub {
  font-size: 12px;
  opacity: 0.8;
  margin-top: 2px;
}

.nav a {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  margin-left: 24px;
  font-size: 14px;
  transition: color 0.2s;
}

.nav a:hover {
  color: #fff;
}

.user-status {
  margin-left: auto;
}

.user-badge {
  display: inline-flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  border-radius: 16px;
  padding: 6px 10px;
  font-size: 13px;
}

.user-badge.guest {
  opacity: 0.9;
}

.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px 48px;
}

.hero {
  text-align: center;
  padding: 48px 0 32px;
}

.hero h1 {
  font-size: 36px;
  color: #2e7d32;
  margin-bottom: 12px;
}

.hero p {
  font-size: 16px;
  color: #666;
  margin-bottom: 20px;
}

.health-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  background: #f0f0f0;
  color: #666;
}

.health-badge.online {
  background: #e8f5e9;
  color: #2e7d32;
}

.health-badge.offline {
  background: #ffebee;
  color: #c62828;
}

.login-section {
  margin-top: 20px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
}

.products-section {
  margin-top: 16px;
}

.section-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 24px;
}

.footer {
  text-align: center;
  padding: 24px;
  background: #2e7d32;
  color: rgba(255, 255, 255, 0.8);
  font-size: 13px;
}
</style>
