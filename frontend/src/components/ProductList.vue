<template>
  <div class="product-list">
    <div class="toolbar">
      <label>
        分类筛选：
        <select v-model="selectedCategory" @change="handleFilterChange">
          <option value="">全部分类</option>
          <option v-for="category in categories" :key="category.id" :value="String(category.id)">
            {{ category.name }}
          </option>
        </select>
      </label>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <div class="grid">
        <div v-for="product in products" :key="product.id" class="card">
          <img :src="product.image_url || fallbackImage" :alt="product.name" class="card-img" />
          <div class="card-body">
            <span class="category-tag">{{ product.category_name }}</span>
            <h3 class="product-name">{{ product.name }}</h3>
            <p class="product-desc">{{ product.description || '暂无描述' }}</p>
            <div class="product-footer">
              <span class="price">¥{{ product.price }} / {{ product.unit }}</span>
              <span class="seller">🏪 {{ product.seller_name }}</span>
            </div>
            <button class="btn-buy">立即购买</button>
          </div>
        </div>
      </div>

      <div class="pagination" v-if="pagination.total_pages > 1">
        <button :disabled="pagination.page <= 1" @click="changePage(pagination.page - 1)">上一页</button>
        <span>第 {{ pagination.page }} / {{ pagination.total_pages }} 页，共 {{ pagination.total }} 条</span>
        <button :disabled="pagination.page >= pagination.total_pages" @click="changePage(pagination.page + 1)">下一页</button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getCategories, getProducts } from '../api/index.js'

const products = ref([])
const categories = ref([])
const selectedCategory = ref('')
const loading = ref(true)
const error = ref(null)
const fallbackImage = 'https://placehold.co/300x200?text=农产品'
const pagination = ref({
  page: 1,
  page_size: 6,
  total: 0,
  total_pages: 0,
})

async function fetchCategories() {
  const response = await getCategories()
  categories.value = response.data.data
}

async function fetchProducts(page = 1) {
  loading.value = true
  error.value = null
  try {
    const params = {
      page,
      page_size: pagination.value.page_size,
    }
    if (selectedCategory.value) {
      params.category_id = Number(selectedCategory.value)
    }

    const response = await getProducts(params)
    products.value = response.data.data.items
    pagination.value = response.data.data.pagination
  } catch (err) {
    error.value = '获取商品列表失败，请检查后端服务是否启动'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function handleFilterChange() {
  fetchProducts(1)
}

function changePage(page) {
  fetchProducts(page)
}

function refreshProducts() {
  fetchProducts(1)
}

defineExpose({ refreshProducts })

onMounted(async () => {
  try {
    await fetchCategories()
    await fetchProducts(1)
  } catch (err) {
    error.value = '初始化商品数据失败'
    loading.value = false
    console.error(err)
  }
})
</script>

<style scoped>
.product-list {
  width: 100%;
}

.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}

.toolbar select {
  margin-left: 8px;
  padding: 6px 8px;
  border-radius: 6px;
  border: 1px solid #ddd;
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

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.pagination button {
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 6px;
  padding: 6px 10px;
  cursor: pointer;
}

.pagination button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
