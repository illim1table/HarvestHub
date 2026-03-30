<template>
  <div class="publish-form">
    <h3>发布商品</h3>
    <form @submit.prevent="submitForm">
      <div class="row">
        <input v-model="form.name" placeholder="商品名称" required />
        <input v-model.number="form.price" type="number" min="0.01" step="0.01" placeholder="价格" required />
      </div>
      <div class="row">
        <input v-model="form.unit" placeholder="单位（如：斤）" required />
        <input v-model.number="form.stock" type="number" min="0" placeholder="库存" required />
      </div>
      <div class="row">
        <select v-model.number="form.category_id" required>
          <option :value="0" disabled>请选择分类</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
        </select>
        <input v-model="form.image_url" placeholder="图片地址（可选）" />
      </div>
      <textarea v-model="form.description" placeholder="商品描述"></textarea>
      <button type="submit" :disabled="submitting">{{ submitting ? '发布中...' : '发布商品' }}</button>
      <p v-if="message" class="message">{{ message }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { createProduct, getCategories } from '../api/index.js'

const emit = defineEmits(['created'])

const categories = ref([])
const submitting = ref(false)
const message = ref('')
const error = ref('')
const form = ref({
  name: '',
  description: '',
  price: 0,
  unit: '',
  stock: 0,
  image_url: '',
  category_id: 0,
})

async function loadCategories() {
  const response = await getCategories()
  categories.value = response.data.data
}

function resetForm() {
  form.value = {
    name: '',
    description: '',
    price: 0,
    unit: '',
    stock: 0,
    image_url: '',
    category_id: 0,
  }
}

async function submitForm() {
  submitting.value = true
  message.value = ''
  error.value = ''
  try {
    await createProduct({ ...form.value, image_url: form.value.image_url || null })
    message.value = '商品发布成功'
    resetForm()
    emit('created')
  } catch (err) {
    error.value = err?.response?.data?.detail || '商品发布失败，请确认已使用 seller 账号登录'
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  try {
    await loadCategories()
  } catch {
    error.value = '分类加载失败'
  }
})
</script>

<style scoped>
.publish-form {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.publish-form h3 {
  margin-bottom: 12px;
  color: #2e7d32;
}

.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 10px;
}

input,
select,
textarea,
button {
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 8px;
  font-size: 14px;
}

textarea {
  min-height: 72px;
  margin-bottom: 10px;
}

button {
  background: #2e7d32;
  color: #fff;
  border: none;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message {
  color: #2e7d32;
  margin-top: 10px;
}

.error {
  color: #e74c3c;
  margin-top: 10px;
}
</style>
