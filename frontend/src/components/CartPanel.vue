<template>
  <div class="cart-panel">
    <h3>购物车</h3>
    <p v-if="!items.length" class="empty">购物车为空</p>
    <div v-else class="cart-items">
      <div class="cart-item" v-for="item in items" :key="item.product_id">
        <div>
          <div class="name">{{ item.product_name }}</div>
          <div class="meta">¥{{ item.price }} × {{ item.quantity }}</div>
        </div>
        <button @click="$emit('remove', item.product_id)">移除</button>
      </div>
      <div class="total">预估总价：¥{{ totalAmount }}</div>
      <button class="submit-btn" :disabled="submitting" @click="$emit('submit')">
        {{ submitting ? '下单中...' : '提交订单' }}
      </button>
    </div>
    <p v-if="message" class="message">{{ message }}</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  totalAmount: {
    type: [String, Number],
    default: '0.00',
  },
  submitting: {
    type: Boolean,
    default: false,
  },
  message: {
    type: String,
    default: '',
  },
  error: {
    type: String,
    default: '',
  },
})

defineEmits(['remove', 'submit'])
</script>

<style scoped>
.cart-panel {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.empty {
  color: #888;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cart-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  padding: 10px;
}

.name {
  font-weight: 600;
}

.meta {
  color: #666;
  font-size: 13px;
  margin-top: 4px;
}

.total {
  font-weight: 700;
  color: #2e7d32;
}

.submit-btn {
  border: none;
  border-radius: 8px;
  padding: 10px;
  background: #2e7d32;
  color: #fff;
  cursor: pointer;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message {
  color: #2e7d32;
  margin-top: 10px;
}

.error {
  color: #e53935;
  margin-top: 10px;
}
</style>
