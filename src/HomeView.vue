<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchInput = ref('')

// 工具列表
const tools = ref([
  { id: 'workflow', name: '工作流', icon: '⚡', path: '/workflow' },
  { id: 'model', name: '模型管理', icon: '📦', path: '/models' },
  { id: 'history', name: '历史记录', icon: '📜', path: '/history' },
  { id: 'settings', name: '设置', icon: '⚙️', path: '/settings' },
  { id: 'community', name: '社区', icon: '🌐', path: '/community' },
  { id: 'docs', name: '文档', icon: '📖', path: '/docs' },
])

const handleSearch = () => {
  if (searchInput.value.trim()) {
    console.log('Search:', searchInput.value)
  }
}

const openTool = (path: string) => {
  router.push(path)
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
          <a href="#" class="nav-link">工作流</a>
          <a href="#" class="nav-link">模板</a>
          <a href="#" class="nav-link">社区</a>
          <a href="#" class="nav-link">文档</a>
        </nav>
        <div class="nav-actions">
          <button class="btn-ghost">登录</button>
          <button class="btn-primary">开始使用</button>
        </div>
      </div>
    </header>

    <!-- Hero 主区域 -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          视觉 AI 的 <span class="highlight">最强可控性</span>
        </h1>
        <p class="hero-subtitle">
          精确掌控每个模型、每个参数和每个输出
        </p>

        <!-- 输入栏 -->
        <div class="search-section">
          <div class="search-bar">
            <span class="search-icon">🔍</span>
            <input
              v-model="searchInput"
              type="text"
              class="search-input"
              placeholder="输入提示词或描述你想要生成的..."
              @keyup.enter="handleSearch"
            />
            <button class="search-btn" @click="handleSearch">
              <span>生成 ▶</span>
            </button>
          </div>
        </div>

        <!-- 快速操作 -->
        <div class="quick-actions">
          <button class="quick-btn" @click="handleSearch">
            <span class="quick-icon">⚡</span>
            <span>运行你的第一个工作流</span>
          </button>
          <button class="quick-btn secondary">
            <span class="quick-icon">📂</span>
            <span>加载模板</span>
          </button>
        </div>
      </div>
    </section>

    <!-- 功能面板 -->
    <section class="tools-section">
      <div class="tools-container">
        <div class="tools-header">
          <h2 class="tools-title">工具面板</h2>
          <p class="tools-desc">从这些工具开始你的 AI 创作之旅</p>
        </div>
        <div class="tools-grid">
          <button
            v-for="tool in tools"
            :key="tool.id"
            class="tool-card"
            @click="openTool(tool.path)"
          >
            <span class="tool-icon">{{ tool.icon }}</span>
            <span class="tool-name">{{ tool.name }}</span>
          </button>
        </div>
      </div>
    </section>

    <!-- 底部 -->
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
}

.nav-link:hover {
  color: #fff;
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

/* ========== Hero 区域 ========== */
.hero {
  flex: 1;
  padding: 100px 32px 80px;
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
  font-size: 64px;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 24px;
  letter-spacing: -0.02em;
}

.highlight {
  color: #FFD500;
}

.hero-subtitle {
  font-size: 20px;
  color: #999;
  margin-bottom: 48px;
  line-height: 1.5;
}

/* ========== 搜索栏 ========== */
.search-section {
  margin-bottom: 32px;
}

.search-bar {
  display: flex;
  align-items: center;
  background: #0a0a0a;
  border: 1px solid #2a2a2a;
  border-radius: 12px;
  padding: 6px;
  max-width: 720px;
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

/* ========== 快速操作 ========== */
.quick-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.quick-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #0a0a0a;
  border: 1px solid #2a2a2a;
  color: #fff;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.quick-btn:hover {
  border-color: #FFD500;
  background: #111;
}

.quick-icon {
  font-size: 16px;
}

/* ========== 工具面板 ========== */
.tools-section {
  padding: 80px 32px;
  background: #0a0a0a;
  border-top: 1px solid #1a1a1a;
}

.tools-container {
  max-width: 1200px;
  margin: 0 auto;
}

.tools-header {
  text-align: center;
  margin-bottom: 48px;
}

.tools-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #fff;
}

.tools-desc {
  font-size: 16px;
  color: #888;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
}

.tool-card {
  background: #111;
  border: 1px solid #2a2a2a;
  border-radius: 12px;
  padding: 32px 20px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  transition: all 0.2s;
}

.tool-card:hover {
  background: #1a1a1a;
  border-color: #FFD500;
  transform: translateY(-2px);
}

.tool-icon {
  font-size: 32px;
}

.tool-name {
  font-size: 14px;
  color: #ddd;
  font-weight: 500;
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
