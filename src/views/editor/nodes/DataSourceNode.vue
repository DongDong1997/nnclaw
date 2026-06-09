<script setup lang="ts">
import BaseNode from './BaseNode.vue'

defineProps<{
  id: string
  data: {
    label: string
    source?: string
  }
}>()
</script>

<template>
  <BaseNode
    title="数据源"
    icon="📊"
    color="#64B5F6"
    :outputs="[{ id: 'dataset', label: 'dataset' }]"
  >
    <div class="param-row">
      <span class="param-label">数据集</span>
      <span class="param-value">{{ data.source || 'iris' }}</span>
    </div>
  </BaseNode>
</template>

<style scoped>
.param-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.param-label {
  color: #888;
  font-size: 11px;
}

.param-value {
  color: #64B5F6;
  font-size: 11px;
  font-weight: 500;
}
</style>
