<template>
  <div class="orders-panel">
    <h3>我的订单</h3>
    <button class="refresh-btn" @click="loadOrders" :disabled="loading">
      {{ loading ? '刷新中...' : '刷新订单' }}
    </button>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="!loading && !orders.length" class="empty">暂无订单</p>

    <div v-for="order in orders" :key="order.id" class="order-card">
      <div class="order-head">
        <span>订单 #{{ order.id }}</span>
        <span>状态：{{ order.status }}</span>
      </div>
      <div class="order-meta">
        <span>金额：¥{{ order.total_amount }}</span>
        <span>创建时间：{{ formatDate(order.created_at) }}</span>
      </div>
      <ul class="items">
        <li v-for="item in order.items" :key="item.id">
          {{ item.product_name }}：¥{{ item.price }} × {{ item.quantity }} = ¥{{ item.amount }}
        </li>
      </ul>
      <div class="actions">
        <button v-if="order.status === 'pending'" @click="cancel(order.id)" :disabled="cancellingId === order.id">
          {{ cancellingId === order.id ? '取消中...' : '取消订单' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { cancelOrder, getOrders } from '../api/index.js'

const orders = ref([])
const loading = ref(false)
const error = ref('')
const cancellingId = ref(0)

function formatDate(value) {
  try {
    return new Date(value).toLocaleString()
  } catch {
    return value
  }
}

async function loadOrders() {
  loading.value = true
  error.value = ''
  try {
    const response = await getOrders()
    orders.value = response.data.data.items
  } catch (err) {
    error.value = err?.response?.data?.detail || '订单加载失败，请先登录买家账号'
  } finally {
    loading.value = false
  }
}

async function cancel(id) {
  cancellingId.value = id
  error.value = ''
  try {
    await cancelOrder(id)
    await loadOrders()
  } catch (err) {
    error.value = err?.response?.data?.detail || '取消订单失败'
  } finally {
    cancellingId.value = 0
  }
}

defineExpose({ loadOrders })

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.orders-panel {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-top: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.refresh-btn {
  margin: 8px 0 12px;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 8px;
  padding: 6px 10px;
  cursor: pointer;
}

.order-card {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 12px;
  margin-top: 10px;
}

.order-head,
.order-meta {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.order-meta {
  margin-top: 6px;
  color: #666;
  font-size: 13px;
}

.items {
  margin: 10px 0 0 18px;
}

.actions {
  margin-top: 10px;
}

.actions button {
  border: none;
  border-radius: 6px;
  padding: 6px 10px;
  background: #e53935;
  color: #fff;
  cursor: pointer;
}

.empty {
  color: #888;
}

.error {
  color: #e53935;
}
</style>
