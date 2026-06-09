<script setup lang="ts">
import BaseNode from './BaseNode.vue'

defineProps<{
  id: string
  data: {
    label: string
  }
}>()
</script>

<template>
  <BaseNode
    title="可视化"
    icon="🎨"
    color="#FF9CF9"
    :inputs="[{ id: 'metrics', label: 'metrics' }]"
  >
    <div class="param-row">
      <span class="param-label">图表</span>
      <span class="param-value">混淆矩阵</span>
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
  color: #FF9CF9;
  font-size: 11px;
  font-weight: 500;
}
</style>
