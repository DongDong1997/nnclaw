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
    title="模型评估"
    icon="📈"
    color="#FFA931"
    :inputs="[
      { id: 'model', label: 'model' },
      { id: 'X_test', label: 'X_test' },
      { id: 'y_test', label: 'y_test' },
    ]"
    :outputs="[{ id: 'metrics', label: 'metrics' }]"
  >
    <div class="param-row">
      <span class="param-label">指标</span>
      <span class="param-value">accuracy, f1</span>
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
  color: #FFA931;
  font-size: 11px;
  font-weight: 500;
}
</style>
