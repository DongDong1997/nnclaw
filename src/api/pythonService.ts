/**
 * NNClaw - Python ML Service API 客户端
 * 直接与 FastAPI 后端通信（无 Node.js 中间层）
 */

const PYTHON_BASE = import.meta.env.VITE_PYTHON_URL || 'http://localhost:8000'

export interface MLNode {
  id: string
  type: string
  params?: Record<string, any>
  position?: { x: number; y: number }
}

export interface MLEdge {
  source: string
  target: string
  sourceHandle?: string | null
  targetHandle?: string | null
}

export interface WorkflowPayload {
  nodes: MLNode[]
  edges: MLEdge[]
}

export interface TaskResponse {
  task_id: string
  status: string
}

export interface TaskDetail {
  id: string
  status: 'pending' | 'running' | 'success' | 'failed' | 'cancelled'
  workflow: WorkflowPayload
  nodeStatuses: Record<string, { status: string; startedAt?: string; finishedAt?: string; error?: string }>
  results: Record<string, any>
  startedAt?: string
  finishedAt?: string
  error?: string
}

/**
 * 提交工作流执行
 */
export async function runWorkflow(payload: WorkflowPayload): Promise<TaskResponse> {
  const resp = await fetch(`${PYTHON_BASE}/api/workflows/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!resp.ok) {
    throw new Error(`Run failed: ${resp.status} ${await resp.text()}`)
  }
  return resp.json()
}

/**
 * 查询任务状态
 */
export async function getTask(taskId: string): Promise<TaskDetail> {
  const resp = await fetch(`${PYTHON_BASE}/api/tasks/${taskId}`)
  if (!resp.ok) {
    throw new Error(`Get task failed: ${resp.status}`)
  }
  return resp.json()
}

/**
 * 取消任务
 */
export async function cancelTask(taskId: string): Promise<void> {
  await fetch(`${PYTHON_BASE}/api/tasks/${taskId}/cancel`, { method: 'POST' })
}

/**
 * 列出所有可用节点类型
 */
export async function listNodes(): Promise<{ nodes: Array<{ type: string; schema: any }> }> {
  const resp = await fetch(`${PYTHON_BASE}/api/nodes`)
  if (!resp.ok) {
    throw new Error(`List nodes failed: ${resp.status}`)
  }
  return resp.json()
}

/**
 * 订阅任务进度 (WebSocket)
 */
export function subscribeTaskProgress(
  taskId: string,
  onMessage: (task: TaskDetail) => void,
  onError?: (err: Event) => void,
): WebSocket {
  const wsUrl = PYTHON_BASE.replace(/^http/, 'ws')
  const ws = new WebSocket(`${wsUrl}/ws/tasks/${taskId}`)

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      onMessage(data)
    } catch (e) {
      console.error('Failed to parse WS message:', e)
    }
  }
  ws.onerror = (err) => {
    console.error('WS error:', err)
    onError?.(err)
  }
  return ws
}

/**
 * 健康检查
 */
export async function healthCheck(): Promise<boolean> {
  try {
    const resp = await fetch(`${PYTHON_BASE}/api/health`)
    return resp.ok
  } catch {
    return false
  }
}
