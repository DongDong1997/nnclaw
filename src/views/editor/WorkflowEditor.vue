<script setup lang="ts">
import { ref, markRaw, onMounted } from 'vue'
import { VueFlow, useVueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import type { Node, Edge, Connection } from '@vue-flow/core'
import { runWorkflow, subscribeTaskProgress, cancelTask } from '../../api/pythonService'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import '@vue-flow/controls/dist/style.css'
import '@vue-flow/minimap/dist/style.css'

import DataSourceNode from './nodes/DataSourceNode.vue'
import PreprocessNode from './nodes/PreprocessNode.vue'
import TrainNode from './nodes/TrainNode.vue'
import EvaluateNode from './nodes/EvaluateNode.vue'
import VisualizeNode from './nodes/VisualizeNode.vue'


const nodeTypes = {
  data_source: markRaw(DataSourceNode),
  preprocess: markRaw(PreprocessNode),
  train: markRaw(TrainNode),
  evaluate: markRaw(EvaluateNode),
  visualize: markRaw(VisualizeNode),
}

const initialNodes: Node[] = [
  {
    id: '1',
    type: 'data_source',
    position: { x: 50, y: 100 },
    data: { label: 'Iris 数据集', source: 'sklearn.datasets.load_iris' },
  },
  {
    id: '2',
    type: 'preprocess',
    position: { x: 350, y: 100 },
    data: { label: '数据划分', params: { test_size: 0.2, random_state: 42 } },
  },
  {
    id: '3',
    type: 'train',
    position: { x: 650, y: 100 },
    data: { label: '随机森林', params: { n_estimators: 100, max_depth: 5 } },
  },
  {
    id: '4',
    type: 'evaluate',
    position: { x: 950, y: 50 },
    data: { label: '评估指标' },
  },
  {
    id: '5',
    type: 'visualize',
    position: { x: 950, y: 200 },
    data: { label: '混淆矩阵' },
  },
]

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#FFD500' } },
  { id: 'e2-3', source: '2', target: '3', animated: true, style: { stroke: '#FFD500' } },
  { id: 'e3-4', source: '3', target: '4', animated: true, style: { stroke: '#FFD500' } },
  { id: 'e3-5', source: '3', target: '5', animated: true, style: { stroke: '#FFD500' } },
]

const nodes = ref<Node[]>(initialNodes)
const edges = ref<Edge[]>(initialEdges)

const { onConnect, addNodes } = useVueFlow()

onConnect((connection: Connection) => {
  edges.value = [
    ...edges.value,
    {
      ...connection,
      id: `e${connection.source}-${connection.target}-${Date.now()}`,
      animated: true,
      style: { stroke: '#FFD500' },
    } as Edge,
  ]
})

// 节点面板
const nodePalette = [
  { type: 'data_source', label: '数据源', icon: '📊', color: '#64B5F6' },
  { type: 'preprocess', label: '数据预处理', icon: '⚙️', color: '#6EE7B7' },
  { type: 'train', label: '模型训练', icon: '🧠', color: '#B39DDB' },
  { type: 'evaluate', label: '模型评估', icon: '📈', color: '#FFA931' },
  { type: 'visualize', label: '可视化', icon: '🎨', color: '#FF9CF9' },
]

let nodeIdCounter = 100
const onDragStart = (event: DragEvent, type: string) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('application/vueflow', type)
    event.dataTransfer.effectAllowed = 'move'
  }
}

const onDragOver = (event: DragEvent) => {
  event.preventDefault()
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = 'move'
  }
}

const onDrop = (event: DragEvent) => {
  event.preventDefault()
  const type = event.dataTransfer?.getData('application/vueflow')
  if (!type) return

  const paletteItem = nodePalette.find((n) => n.type === type)
  if (!paletteItem) return

  const position = { x: event.offsetX, y: event.offsetY }
  const newNode: Node = {
    id: `n${++nodeIdCounter}`,
    type,
    position,
    data: { label: paletteItem.label, params: {} },
  }
  nodes.value = [...nodes.value, newNode]
}

// 运行状态
const isRunning = ref(false)
const runProgress = ref(0)
const runStatus = ref<string>('就绪')
const runResults = ref<Record<string, any> | null>(null)
const currentTaskId = ref<string | null>(null)
let currentWs: WebSocket | null = null

const runWorkflowAction = async () => {
  if (isRunning.value) {
    // 取消运行
    if (currentTaskId.value) await cancelTask(currentTaskId.value)
    isRunning.value = false
    runStatus.value = '已取消'
    currentWs?.close()
    return
  }

  isRunning.value = true
  runProgress.value = 0
  runResults.value = null
  runStatus.value = '提交任务...'

  // 构造工作流 payload
  const payload = {
    nodes: nodes.value.map((n) => ({
      id: n.id,
      type: n.type || 'data_source',
      params: n.data?.params || {},
      position: n.position,
    })),
    edges: edges.value.map((e) => ({
      source: e.source,
      target: e.target,
      sourceHandle: e.sourceHandle || null,
      targetHandle: e.targetHandle || null,
    })),
  }

  try {
    const { task_id } = await runWorkflow(payload)
    currentTaskId.value = task_id
    runStatus.value = '执行中...'

    // 订阅 WebSocket 进度
    currentWs = subscribeTaskProgress(
      task_id,
      (task) => {
        // 计算进度
        const total = Object.keys(task.nodeStatuses || {}).length || 1
        const done = Object.values(task.nodeStatuses || {}).filter(
          (n: any) => n.status === 'success' || n.status === 'failed',
        ).length
        runProgress.value = Math.round((done / total) * 100)

        const running = Object.entries(task.nodeStatuses || {}).find(
          ([, s]: [string, any]) => s.status === 'running',
        )
        if (running) {
          runStatus.value = `执行节点 ${running[0]}...`
        }

        if (task.status === 'success') {
          runStatus.value = '完成 ✓'
          runProgress.value = 100
          runResults.value = task.results
          isRunning.value = false
          currentWs?.close()
        } else if (task.status === 'failed') {
          runStatus.value = `失败: ${task.error || ''}`
          isRunning.value = false
          currentWs?.close()
        }
      },
    )
  } catch (e: any) {
    runStatus.value = `错误: ${e.message}`
    isRunning.value = false
  }
}

// 兼容旧引用
const runWorkflow = runWorkflowAction
// (上面 runWorkflowAction 已绑定到 runWorkflow 用于模板 @click)

const saveWorkflow = () => {
  const workflow = {
    nodes: nodes.value,
    edges: edges.value,
  }
  console.log('保存工作流:', JSON.stringify(workflow, null, 2))
  alert('工作流已保存到控制台')
}

onMounted(() => {
  console.log('工作流编辑器已挂载')
})
</script>

<template>
  <div class="editor-page">
    <!-- 顶部工具栏 -->
    <header class="editor-header">
      <div class="header-left">
        <router-link to="/" class="back-btn">← 返回</router-link>
        <span class="workflow-name">ML Pipeline · Iris 分类示例</span>
      </div>
      <div class="header-right">
        <button class="btn-secondary" @click="saveWorkflow">保存</button>
        <button class="btn-primary" :disabled="isRunning" @click="runWorkflow">
          <span v-if="isRunning">运行中 {{ runProgress }}%</span>
          <span v-else>▶ 运行</span>
        </button>
      </div>
    </header>

    <!-- 运行状态栏 -->
    <div class="status-bar">
      <div class="status-info">
        <span class="status-icon">
          {{ isRunning ? '⏳' : runProgress === 100 ? '✓' : '●' }}
        </span>
        <span>{{ runStatus }}</span>
      </div>
      <div class="progress-bar">
        <div
          class="progress-fill"
          :style="{ width: runProgress + '%', background: runProgress === 100 ? '#22C55E' : 'linear-gradient(90deg, #FFD500, #FFE340)' }"
        ></div>
      </div>
    </div>

    <!-- 运行结果展示 -->
    <div v-if="runResults && !isRunning" class="results-bar">
      <div class="results-tabs">
        <span class="results-title">结果</span>
        <div v-for="(result, nid) in runResults" :key="nid" class="result-item">
          <span class="result-node">节点 {{ nid }}</span>
          <div v-if="result.metrics" class="result-content">
            <div class="metric">
              <span class="metric-label">accuracy</span>
              <span class="metric-value">{{ (result.metrics.accuracy * 100).toFixed(2) }}%</span>
            </div>
            <div class="metric">
              <span class="metric-label">f1 (macro)</span>
              <span class="metric-value">{{ (result.metrics.f1_macro * 100).toFixed(2) }}%</span>
            </div>
          </div>
          <img
            v-if="result.image"
            :src="`data:image/png;base64,${result.image}`"
            class="result-image"
            alt="可视化"
          />
        </div>
      </div>
    </div>

    <!-- 主体 -->
    <div class="editor-body">
      <!-- 节点面板 -->
      <aside class="node-palette">
        <h3 class="palette-title">节点库</h3>
        <div
          v-for="item in nodePalette"
          :key="item.type"
          class="palette-item"
          draggable="true"
          @dragstart="onDragStart($event, item.type)"
          :style="{ borderColor: item.color }"
        >
          <span class="palette-icon" :style="{ color: item.color }">{{ item.icon }}</span>
          <span class="palette-label">{{ item.label }}</span>
        </div>
      </aside>

      <!-- 画布 -->
      <main class="canvas-wrapper" @drop="onDrop" @dragover="onDragOver">
        <VueFlow
          v-model:nodes="nodes"
          v-model:edges="edges"
          :node-types="nodeTypes"
          :default-viewport="{ x: 0, y: 0, zoom: 1 }"
          :min-zoom="0.2"
          :max-zoom="4"
          fit-view-on-init
        >
          <Background pattern-color="#333" :gap="20" />
          <Controls />
          <MiniMap pannable zoomable node-color="#FFD500" mask-color="rgba(0,0,0,0.8)" />
        </VueFlow>
      </main>

      <!-- 节点配置面板 -->
      <aside class="inspector">
        <h3 class="inspector-title">属性</h3>
        <div class="inspector-content">
          <p class="inspector-hint">选中节点查看参数</p>
          <div class="inspector-section">
            <h4>工作流信息</h4>
            <div class="info-row">
              <span>节点数</span>
              <span>{{ nodes.length }}</span>
            </div>
            <div class="info-row">
              <span>连接数</span>
              <span>{{ edges.length }}</span>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.editor-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #0a0a0a;
  color: #fff;
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* 顶部工具栏 */
.editor-header {
  height: 56px;
  padding: 0 20px;
  background: #111;
  border-bottom: 1px solid #2a2a2a;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.header-left,
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.back-btn {
  color: #999;
  text-decoration: none;
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #1a1a1a;
  color: #fff;
}

.workflow-name {
  color: #ddd;
  font-size: 14px;
  font-weight: 500;
}

.btn-secondary {
  background: transparent;
  border: 1px solid #333;
  color: #fff;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #1a1a1a;
  border-color: #555;
}

.btn-primary {
  background: #FFD500;
  border: none;
  color: #000;
  padding: 8px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #FFE340;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 状态栏 */
.status-bar {
  background: #111;
  border-bottom: 1px solid #2a2a2a;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #FFD500;
  min-width: 200px;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: #2a2a2a;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #FFD500, #FFE340);
  transition: width 0.3s;
}

/* 结果展示栏 */
.results-bar {
  background: #111;
  border-bottom: 1px solid #2a2a2a;
  padding: 12px 20px;
  max-height: 200px;
  overflow-y: auto;
}

.results-tabs {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  flex-wrap: wrap;
}

.results-title {
  font-size: 12px;
  color: #FFD500;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding-top: 4px;
  flex-shrink: 0;
}

.result-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 6px;
  padding: 10px 14px;
  min-width: 200px;
}

.result-node {
  font-size: 11px;
  color: #888;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.metric {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.metric-label {
  color: #888;
}

.metric-value {
  color: #FFD500;
  font-weight: 600;
}

.result-image {
  max-width: 240px;
  max-height: 120px;
  border-radius: 4px;
  background: #000;
}

/* 主体三栏 */
.editor-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.node-palette {
  width: 220px;
  background: #0a0a0a;
  border-right: 1px solid #2a2a2a;
  padding: 20px 16px;
  overflow-y: auto;
  flex-shrink: 0;
}

.palette-title,
.inspector-title {
  font-size: 12px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.palette-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: #111;
  border: 1px solid #2a2a2a;
  border-left: 3px solid;
  border-radius: 6px;
  margin-bottom: 8px;
  cursor: grab;
  transition: all 0.2s;
  user-select: none;
}

.palette-item:hover {
  background: #1a1a1a;
  transform: translateX(2px);
}

.palette-item:active {
  cursor: grabbing;
}

.palette-icon {
  font-size: 20px;
}

.palette-label {
  font-size: 13px;
  color: #ddd;
}

/* 画布 */
.canvas-wrapper {
  flex: 1;
  position: relative;
  background: #000;
}

.canvas-wrapper :deep(.vue-flow) {
  background: #000;
}

.canvas-wrapper :deep(.vue-flow__node) {
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

.canvas-wrapper :deep(.vue-flow__controls) {
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 6px;
  overflow: hidden;
}

.canvas-wrapper :deep(.vue-flow__controls-button) {
  background: #1a1a1a;
  border-bottom: 1px solid #2a2a2a;
  color: #FFD500;
  fill: #FFD500;
}

.canvas-wrapper :deep(.vue-flow__controls-button:hover) {
  background: #2a2a2a;
}

.canvas-wrapper :deep(.vue-flow__controls-button svg) {
  fill: #FFD500;
}

.canvas-wrapper :deep(.vue-flow__minimap) {
  background: #111;
  border: 1px solid #2a2a2a;
  border-radius: 6px;
}

/* 检查器 */
.inspector {
  width: 280px;
  background: #0a0a0a;
  border-left: 1px solid #2a2a2a;
  padding: 20px 16px;
  overflow-y: auto;
  flex-shrink: 0;
}

.inspector-content {
  font-size: 13px;
}

.inspector-hint {
  color: #666;
  font-size: 12px;
  padding: 12px;
  background: #111;
  border-radius: 6px;
  text-align: center;
  margin-bottom: 20px;
}

.inspector-section h4 {
  font-size: 12px;
  color: #888;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  background: #111;
  border-radius: 4px;
  margin-bottom: 6px;
  font-size: 13px;
}

.info-row span:first-child {
  color: #888;
}

.info-row span:last-child {
  color: #FFD500;
  font-weight: 600;
}
</style>
