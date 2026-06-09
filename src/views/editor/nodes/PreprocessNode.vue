<script setup lang="ts">
import BaseNode from './BaseNode.vue'

defineProps<{
  id: string
  data: {
    label: string
    params?: {
      test_size?: number
      random_state?: number
    }
  }
}>()
</script>

<template>
  <BaseNode
    title="数据预处理"
    icon="⚙️"
    color="#6EE7B7"
    :inputs="[{ id: 'in', label: 'dataset' }]"
    :outputs="[
      { id: 'X_train', label: 'X_train' },
      { id: 'X_test', label: 'X_test' },
      { id: 'y_train', label: 'y_train' },
      { id: 'y_test', label: 'y_test' },
    ]"
  >
    <div class="param-row">
      <span class="param-label">test_size</span>
      <span class="param-value">{{ data.params?.test_size ?? 0.2 }}</span>
    </div>
    <div class="param-row">
      <span class="param-label">random_state</span>
      <span class="param-value">{{ data.params?.random_state ?? 42 }}</span>
    </div>
  </BaseNode>
</template>

<style scoped>
.param-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.param-row:last-child {
  margin-bottom: 0;
}

.param-label {
  color: #888;
  font-size: 11px;
}

.param-value {
  color: #6EE7B7;
  font-size: 11px;
  font-weight: 500;
}
</style>
