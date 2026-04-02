<template>
  <div class="orders-panel">
    <h3>我的订单</h3>
    <div class="toolbar">
      <select v-model="statusFilter" @change="loadOrders" :disabled="loading">
        <option value="">全部状态</option>
        <option value="pending">待支付</option>
        <option value="paid">已支付</option>
        <option value="completed">已完成</option>
        <option value="cancelled">已取消</option>
      </select>
      <button class="refresh-btn" @click="loadOrders" :disabled="loading">
        {{ loading ? '刷新中...' : '刷新订单' }}
      </button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="message" class="message">{{ message }}</p>
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
      <div class="order-meta">
        <span>支付时间：{{ formatDate(order.paid_at) || '-' }}</span>
        <span>完成时间：{{ formatDate(order.completed_at) || '-' }}</span>
      </div>
      <ul class="items">
        <li v-for="item in order.items" :key="item.id">
          {{ item.product_name }}：¥{{ item.price }} × {{ item.quantity }} = ¥{{ item.amount }}
        </li>
      </ul>
      <div class="actions">
        <button
          v-if="order.status === 'pending'"
          class="cancel-btn"
          @click="cancel(order.id)"
          :disabled="actionOrderId === order.id"
        >
          {{ actionOrderId === order.id ? '处理中...' : '取消订单' }}
        </button>
        <button
          v-if="order.status === 'pending'"
          class="pay-btn"
          @click="mockPay(order.id)"
          :disabled="actionOrderId === order.id"
        >
          {{ actionOrderId === order.id ? '处理中...' : '去支付（模拟）' }}
        </button>
        <button
          v-if="order.status === 'paid'"
          class="confirm-btn"
          @click="confirm(order.id)"
          :disabled="actionOrderId === order.id"
        >
          {{ actionOrderId === order.id ? '处理中...' : '确认收货' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { cancelOrder, confirmOrder, getOrders, mockPayOrder } from '../api/index.js'

const orders = ref([])
const loading = ref(false)
const error = ref('')
const message = ref('')
const actionOrderId = ref(0)
const statusFilter = ref('')

function formatDate(value) {
  if (!value) return ''
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
    const params = statusFilter.value ? { status: statusFilter.value } : {}
    const response = await getOrders(params)
    orders.value = response.data.data.items
  } catch (err) {
    error.value = err?.response?.data?.detail || '订单加载失败，请先登录买家账号'
  } finally {
    loading.value = false
  }
}

async function cancel(id) {
  actionOrderId.value = id
  error.value = ''
  message.value = ''
  try {
    await cancelOrder(id)
    message.value = '订单取消成功'
    await loadOrders()
  } catch (err) {
    error.value = err?.response?.data?.detail || '取消订单失败'
  } finally {
    actionOrderId.value = 0
  }
}

async function mockPay(id) {
  actionOrderId.value = id
  error.value = ''
  message.value = ''
  try {
    const tradeNo = `MOCK-${id}-${Date.now()}`
    const res = await mockPayOrder({
      order_id: id,
      trade_no: tradeNo,
      pay_status: 'success',
    })
    message.value = res?.data?.message || '模拟支付成功'
    await loadOrders()
  } catch (err) {
    error.value = err?.response?.data?.detail || '模拟支付失败'
  } finally {
    actionOrderId.value = 0
  }
}

async function confirm(id) {
  actionOrderId.value = id
  error.value = ''
  message.value = ''
  try {
    await confirmOrder(id)
    message.value = '确认收货成功'
    await loadOrders()
  } catch (err) {
    error.value = err?.response?.data?.detail || '确认收货失败'
  } finally {
    actionOrderId.value = 0
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

.toolbar {
  margin: 8px 0 12px;
  display: flex;
  gap: 8px;
}

.toolbar select,
.refresh-btn {
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 8px;
  padding: 6px 10px;
}

.refresh-btn {
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
  display: flex;
  gap: 8px;
}

.actions button {
  border: none;
  border-radius: 6px;
  padding: 6px 10px;
  color: #fff;
  cursor: pointer;
}

.cancel-btn {
  background: #e53935;
}

.pay-btn {
  background: #1e88e5;
}

.confirm-btn {
  background: #43a047;
}

.empty {
  color: #888;
}

.error {
  color: #e53935;
}

.message {
  color: #2e7d32;
}
</style>
