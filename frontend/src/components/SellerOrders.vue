<template>
  <div class="orders-panel">
    <h3>卖家订单管理</h3>
    <div class="toolbar">
      <select v-model="statusFilter" @change="loadOrders" :disabled="loading">
        <option value="">全部状态</option>
        <option value="pending">待支付</option>
        <option value="paid">已支付</option>
        <option value="completed">已完成</option>
        <option value="cancelled">已取消</option>
      </select>
      <button class="refresh-btn" @click="loadOrders" :disabled="loading">
        {{ loading ? '刷新中...' : '刷新卖家订单' }}
      </button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="!loading && !orders.length" class="empty">暂无相关订单</p>

    <div v-for="order in orders" :key="order.id" class="order-card">
      <div class="order-head">
        <span>订单 #{{ order.id }}</span>
        <span>状态：{{ order.status }}</span>
      </div>
      <div class="order-meta">
        <span>金额（整单）：¥{{ order.total_amount }}</span>
        <span>创建时间：{{ formatDate(order.created_at) }}</span>
      </div>
      <ul class="items">
        <li v-for="item in order.items" :key="item.id">
          {{ item.product_name }}：¥{{ item.price }} × {{ item.quantity }} = ¥{{ item.amount }}
        </li>
      </ul>
      <div class="actions">
        <button @click="loadDetail(order.id)" :disabled="detailLoadingId === order.id">
          {{ detailLoadingId === order.id ? '加载中...' : '查看详情' }}
        </button>
      </div>
    </div>

    <div v-if="detail" class="detail-box">
      <h4>订单详情 #{{ detail.id }}</h4>
      <p>状态：{{ detail.status }}</p>
      <p>支付交易号：{{ detail.payment_trade_no || '-' }}</p>
      <p>支付时间：{{ formatDate(detail.paid_at) || '-' }}</p>
      <p>完成时间：{{ formatDate(detail.completed_at) || '-' }}</p>
      <ul>
        <li v-for="item in detail.items" :key="item.id">
          {{ item.product_name }}：¥{{ item.price }} × {{ item.quantity }} = ¥{{ item.amount }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getSellerOrderDetail, getSellerOrders } from '../api/index.js'

const orders = ref([])
const loading = ref(false)
const error = ref('')
const statusFilter = ref('')
const detail = ref(null)
const detailLoadingId = ref(0)

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
    const response = await getSellerOrders(params)
    orders.value = response.data.data.items
  } catch (err) {
    error.value = err?.response?.data?.detail || '卖家订单加载失败（请确认卖家权限）'
  } finally {
    loading.value = false
  }
}

async function loadDetail(id) {
  detailLoadingId.value = id
  error.value = ''
  try {
    const response = await getSellerOrderDetail(id)
    detail.value = response.data.data
  } catch (err) {
    error.value = err?.response?.data?.detail || '加载卖家订单详情失败'
  } finally {
    detailLoadingId.value = 0
  }
}

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
  background: #5e35b1;
  color: #fff;
  cursor: pointer;
}

.detail-box {
  margin-top: 12px;
  border: 1px dashed #bbb;
  border-radius: 8px;
  padding: 12px;
  background: #fafafa;
}

.empty {
  color: #888;
}

.error {
  color: #e53935;
}
</style>
