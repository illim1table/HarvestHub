<template>
  <div class="product-list">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="grid">
      <div v-for="product in products" :key="product.id" class="card">
        <img :src="product.image_url" :alt="product.name" class="card-img" />
        <div class="card-body">
          <span class="category-tag">{{ product.category }}</span>
          <h3 class="product-name">{{ product.name }}</h3>
          <p class="product-desc">{{ product.description }}</p>
          <div class="product-footer">
            <span class="price">¥{{ product.price }} / {{ product.unit }}</span>
            <span class="seller">🏪 {{ product.seller }}</span>
          </div>
          <button class="btn-buy">立即购买</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getProducts } from '../api/index.js'

const products = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const response = await getProducts()
    products.value = response.data
  } catch (err) {
    error.value = '获取商品列表失败，请检查后端服务是否启动'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.product-list {
  width: 100%;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  font-size: 16px;
  color: #666;
}

.error {
  color: #e74c3c;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.card-body {
  padding: 16px;
}

.category-tag {
  display: inline-block;
  background: #e8f5e9;
  color: #2e7d32;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  margin: 6px 0;
  color: #333;
}

.product-desc {
  font-size: 13px;
  color: #888;
  margin: 4px 0 12px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.price {
  font-size: 18px;
  font-weight: 700;
  color: #e53935;
}

.seller {
  font-size: 12px;
  color: #888;
}

.btn-buy {
  width: 100%;
  padding: 10px;
  background: linear-gradient(135deg, #4caf50, #2e7d32);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-buy:hover {
  opacity: 0.9;
}
</style>
