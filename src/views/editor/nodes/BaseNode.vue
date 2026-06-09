<script setup lang="ts">
import { Handle, Position } from '@vue-flow/core'

// 接收 Vue Flow 节点的所有 props
defineProps<{
  id: string
  data: Record<string, any>
  title: string
  icon: string
  color: string
  inputs?: Array<{ id: string; label: string }>
  outputs?: Array<{ id: string; label: string }>
}>()
</script>

<template>
  <div class="ml-node" :style="{ borderColor: color }">
    <!-- 标题栏 -->
    <div class="node-header" :style="{ background: color }">
      <span class="node-icon">{{ icon }}</span>
      <span class="node-title">{{ title }}</span>
    </div>

    <!-- 输入端口 -->
    <div v-if="inputs && inputs.length" class="node-inputs">
      <div v-for="input in inputs" :key="input.id" class="port-row">
        <Handle
          :id="input.id"
          :position="Position.Left"
          type="target"
          :style="{ background: color }"
        />
        <span class="port-label">{{ input.label }}</span>
      </div>
    </div>

    <!-- 主体内容 -->
    <div class="node-body">
      <slot />
    </div>

    <!-- 输出端口 -->
    <div v-if="outputs && outputs.length" class="node-outputs">
      <div v-for="output in outputs" :key="output.id" class="port-row">
        <span class="port-label">{{ output.label }}</span>
        <Handle
          :id="output.id"
          :position="Position.Right"
          type="source"
          :style="{ background: color }"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.ml-node {
  min-width: 200px;
  background: #1a1a1a;
  border: 2px solid;
  border-radius: 8px;
  font-size: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.node-header {
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #000;
  font-weight: 600;
}

.node-icon {
  font-size: 14px;
}

.node-title {
  font-size: 12px;
  flex: 1;
}

.node-body {
  padding: 12px;
  color: #ddd;
}

.node-inputs,
.node-outputs {
  padding: 4px 0;
}

.port-row {
  position: relative;
  padding: 4px 12px;
  display: flex;
  align-items: center;
  min-height: 24px;
}

.port-label {
  font-size: 11px;
  color: #aaa;
  flex: 1;
}

.node-outputs .port-row {
  justify-content: flex-end;
}
</style>
