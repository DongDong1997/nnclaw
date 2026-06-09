<script setup lang="ts">
import BaseNode from './BaseNode.vue'

defineProps<{
  id: string
  data: {
    label: string
    params?: {
      n_estimators?: number
      max_depth?: number
    }
  }
}>()
</script>

<template>
  <BaseNode
    title="模型训练"
    icon="🧠"
    color="#B39DDB"
    :inputs="[
      { id: 'X_train', label: 'X_train' },
      { id: 'y_train', label: 'y_train' },
    ]"
    :outputs="[{ id: 'model', label: 'model' }]"
  >
    <div class="param-row">
      <span class="param-label">算法</span>
      <span class="param-value">RandomForest</span>
    </div>
    <div class="param-row">
      <span class="param-label">n_estimators</span>
      <span class="param-value">{{ data.params?.n_estimators ?? 100 }}</span>
    </div>
    <div class="param-row">
      <span class="param-label">max_depth</span>
      <span class="param-value">{{ data.params?.max_depth ?? 5 }}</span>
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
  color: #B39DDB;
  font-size: 11px;
  font-weight: 500;
}
</style>
