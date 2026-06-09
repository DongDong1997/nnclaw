<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchInput = ref('')

// 模拟工作流列表
const workflows = ref([
  {
    id: 't2i',
    title: '文生图基础工作流',
    desc: '简单的文本到图像生成流程',
    nodes: 5,
    category: '基础',
    color: '#FFD500',
  },
  {
    id: 'i2i',
    title: '图生图工作流',
    desc: '基于参考图生成新图像',
    nodes: 7,
    category: '基础',
    color: '#64B5F6',
  },
  {
    id: 'controlnet',
    title: 'ControlNet 控制',
    desc: '使用 Canny/Depth 控制图像生成',
    nodes: 12,
    category: '高级',
    color: '#6EE7B7',
  },
  {
    id: 'upscale',
    title: '图像超分放大',
    desc: '高清放大低分辨率图像',
    nodes: 4,
    category: '后期',
    color: '#FF9CF9',
  },
  {
    id: 'inpaint',
    title: '局部重绘',
    desc: '基于蒙版重绘指定区域',
    nodes: 6,
    category: '编辑',
    color: '#FFA931',
  },
  {
    id: 'video',
    title: '视频生成',
    desc: '文生视频 / 图生视频',
    nodes: 9,
    category: '高级',
    color: '#B39DDB',
  },
])

const handleSearch = () => {
  if (searchInput.value.trim()) {
    console.log('Search:', searchInput.value)
  }
}

const openWorkflow = (id: string) => {
  console.log('Open workflow:', id)
  router.push('/editor')
}

const newWorkflow = () => {
  router.push('/editor')
}

const goBack = () => {
  router.push('/')
}
</script>

<template>
  <div class="page">
    <!-- 顶部导航栏 -->
    <header class="navbar">
      <div class="nav-inner">
        <div class="brand">
          <span class="brand-icon">◆</span>
          <span class="brand-text">NNClaw</span>
        </div>
        <nav class="nav-menu">
          <a href="#" class="nav-link active">工作流</a>
          <a href="#" class="nav-link">模板</a>
          <a href="#" class="nav-link">社区</a>
          <a href="#" class="nav-link">文档</a>
        </nav>
        <div class="nav-actions">
          <button class="btn-ghost" @click="goBack">返回主页</button>
          <button class="btn-primary" @click="newWorkflow">新建工作流</button>
        </div>
      </div>
    </header>

    <!-- Hero 区域 -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          探索 <span class="highlight">工作流</span>
        </h1>
        <p class="hero-subtitle">
          在画布上连接模型、处理步骤和输出，每个决策都可见，每个步骤都可检查
        </p>

        <!-- 搜索栏 -->
        <div class="search-section">
          <div class="search-bar">
            <span class="search-icon">🔍</span>
            <input
              v-model="searchInput"
              type="text"
              class="search-input"
              placeholder="搜索工作流模板..."
              @keyup.enter="handleSearch"
            />
            <button class="search-btn" @click="handleSearch">搜索</button>
          </div>
        </div>

        <!-- 分类筛选 -->
        <div class="categories">
          <button class="category-btn active">全部</button>
          <button class="category-btn">基础</button>
          <button class="category-btn">高级</button>
          <button class="category-btn">编辑</button>
          <button class="category-btn">后期</button>
        </div>
      </div>
    </section>

    <!-- 工作流列表 -->
    <section class="workflows-section">
      <div class="workflows-container">
        <div class="section-header">
          <h2 class="section-title">精选工作流</h2>
          <button class="view-all">查看全部 →</button>
        </div>

        <div class="workflows-grid">
          <article
            v-for="wf in workflows"
            :key="wf.id"
            class="workflow-card"
            @click="openWorkflow(wf.id)"
          >
            <div class="wf-preview">
              <div class="preview-canvas">
                <div class="node" :style="{ top: '20%', left: '10%', borderColor: wf.color }">
                  <div class="node-title">Load Model</div>
                </div>
                <div class="node" :style="{ top: '20%', left: '50%', borderColor: wf.color }">
                  <div class="node-title">Prompt</div>
                </div>
                <div class="node" :style="{ top: '60%', left: '30%', borderColor: wf.color }">
                  <div class="node-title">Sampler</div>
                </div>
                <div class="node" :style="{ top: '60%', left: '65%', borderColor: wf.color }">
                  <div class="node-title">Output</div>
                </div>
                <svg class="connectors" viewBox="0 0 100 100" preserveAspectRatio="none">
                  <line x1="30" y1="25" x2="60" y2="25" stroke="#FFD500" stroke-width="0.3" />
                  <line x1="30" y1="25" x2="40" y2="65" stroke="#FFD500" stroke-width="0.3" />
                  <line x1="60" y1="25" x2="40" y2="65" stroke="#FFD500" stroke-width="0.3" />
                  <line x1="40" y1="65" x2="75" y2="65" stroke="#FFD500" stroke-width="0.3" />
                </svg>
              </div>
            </div>
            <div class="wf-info">
              <div class="wf-meta">
                <span class="wf-category" :style="{ color: wf.color, borderColor: wf.color }">
                  {{ wf.category }}
                </span>
                <span class="wf-nodes">{{ wf.nodes }} 节点</span>
              </div>
              <h3 class="wf-title">{{ wf.title }}</h3>
              <p class="wf-desc">{{ wf.desc }}</p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- 步骤介绍 -->
    <section class="steps-section">
      <div class="steps-container">
        <h2 class="section-title">几分钟即可上手</h2>
        <p class="section-desc">想多深入就多深入</p>
        <div class="steps-grid">
          <div class="step">
            <div class="step-num">1</div>
            <h3 class="step-title">下载或注册</h3>
            <p class="step-desc">下载本地版或启动云端</p>
          </div>
          <div class="step">
            <div class="step-num">2</div>
            <h3 class="step-title">加载工作流</h3>
            <p class="step-desc">从社区模板开始，或自行构建</p>
          </div>
          <div class="step">
            <div class="step-num">3</div>
            <h3 class="step-title">生成与迭代</h3>
            <p class="step-desc">运行、调整，准备好了就扩展</p>
          </div>
        </div>
      </div>
    </section>

    <footer class="footer">
      <p>© 2026 NNClaw · 精确掌控 AI 创作的每个步骤</p>
    </footer>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.page {
  min-height: 100vh;
  background: #000000;
  color: #ffffff;
  font-family: 'Inter', 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  display: flex;
  flex-direction: column;
}

/* ========== 导航栏 ========== */
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  height: 64px;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid #1a1a1a;
}

.nav-inner {
  max-width: 1280px;
  margin: 0 auto;
  height: 100%;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand-icon {
  font-size: 22px;
  color: #FFD500;
}

.brand-text {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
}

.nav-menu {
  display: flex;
  gap: 32px;
}

.nav-link {
  color: #999;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
  padding-bottom: 4px;
  border-bottom: 2px solid transparent;
}

.nav-link:hover,
.nav-link.active {
  color: #fff;
  border-bottom-color: #FFD500;
}

.nav-actions {
  display: flex;
  gap: 12px;
}

.btn-ghost {
  background: transparent;
  border: 1px solid #333;
  color: #fff;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.btn-ghost:hover {
  background: #1a1a1a;
  border-color: #555;
}

.btn-primary {
  background: #FFD500;
  border: none;
  color: #000;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: #FFE340;
}

/* ========== Hero ========== */
.hero {
  padding: 80px 32px 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  max-width: 900px;
  width: 100%;
  text-align: center;
}

.hero-title {
  font-size: 56px;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 20px;
  letter-spacing: -0.02em;
}

.highlight {
  color: #FFD500;
}

.hero-subtitle {
  font-size: 18px;
  color: #999;
  margin-bottom: 40px;
  line-height: 1.5;
}

/* ========== 搜索栏 ========== */
.search-section {
  margin-bottom: 24px;
}

.search-bar {
  display: flex;
  align-items: center;
  background: #0a0a0a;
  border: 1px solid #2a2a2a;
  border-radius: 12px;
  padding: 6px;
  max-width: 640px;
  margin: 0 auto;
  transition: border-color 0.2s;
}

.search-bar:focus-within {
  border-color: #FFD500;
}

.search-icon {
  padding: 0 12px;
  color: #666;
  font-size: 16px;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #fff;
  font-size: 15px;
  padding: 14px 0;
}

.search-input::placeholder {
  color: #555;
}

.search-btn {
  background: #FFD500;
  border: none;
  color: #000;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.2s;
}

.search-btn:hover {
  background: #FFE340;
}

/* ========== 分类筛选 ========== */
.categories {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}

.category-btn {
  background: transparent;
  border: 1px solid #2a2a2a;
  color: #999;
  padding: 6px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.category-btn:hover {
  border-color: #FFD500;
  color: #fff;
}

.category-btn.active {
  background: #FFD500;
  color: #000;
  border-color: #FFD500;
  font-weight: 600;
}

/* ========== 工作流列表 ========== */
.workflows-section {
  padding: 60px 32px;
}

.workflows-container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.section-title {
  font-size: 28px;
  font-weight: 600;
  color: #fff;
}

.view-all {
  background: transparent;
  border: none;
  color: #FFD500;
  cursor: pointer;
  font-size: 14px;
  transition: opacity 0.2s;
}

.view-all:hover {
  opacity: 0.8;
}

.workflows-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.workflow-card {
  background: #0a0a0a;
  border: 1px solid #2a2a2a;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}

.workflow-card:hover {
  border-color: #FFD500;
  transform: translateY(-2px);
}

.wf-preview {
  position: relative;
  height: 180px;
  background: #111;
  border-bottom: 1px solid #2a2a2a;
  overflow: hidden;
}

.preview-canvas {
  position: relative;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 20px 20px;
}

.node {
  position: absolute;
  background: #1a1a1a;
  border: 1px solid #FFD500;
  border-radius: 4px;
  padding: 6px 10px;
  font-size: 10px;
  min-width: 60px;
  text-align: center;
}

.node-title {
  color: #ddd;
  font-size: 9px;
  white-space: nowrap;
}

.connectors {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.wf-info {
  padding: 20px;
}

.wf-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.wf-category {
  font-size: 11px;
  padding: 2px 8px;
  border: 1px solid;
  border-radius: 4px;
  font-weight: 500;
}

.wf-nodes {
  font-size: 12px;
  color: #666;
}

.wf-title {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 8px;
}

.wf-desc {
  font-size: 13px;
  color: #999;
  line-height: 1.5;
}

/* ========== 步骤介绍 ========== */
.steps-section {
  padding: 80px 32px;
  background: #0a0a0a;
  border-top: 1px solid #1a1a1a;
  text-align: center;
}

.steps-container {
  max-width: 1000px;
  margin: 0 auto;
}

.section-desc {
  font-size: 16px;
  color: #888;
  margin-bottom: 48px;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
}

.step {
  padding: 32px 24px;
  background: #111;
  border: 1px solid #2a2a2a;
  border-radius: 12px;
  transition: all 0.2s;
}

.step:hover {
  border-color: #FFD500;
}

.step-num {
  display: inline-block;
  width: 40px;
  height: 40px;
  line-height: 40px;
  background: #FFD500;
  color: #000;
  border-radius: 50%;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
}

.step-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #fff;
}

.step-desc {
  font-size: 14px;
  color: #888;
  line-height: 1.5;
}

/* ========== 底部 ========== */
.footer {
  padding: 32px;
  text-align: center;
  border-top: 1px solid #1a1a1a;
  color: #666;
  font-size: 13px;
}
</style>
