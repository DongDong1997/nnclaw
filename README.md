<div align="center">

# 🐾 NNClaw

### _Visual ML Pipeline · 让机器学习像搭积木一样简单_

<br/>

![Vue](https://img.shields.io/badge/Vue-3.5-42b883?style=for-the-badge&logo=vue.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-6.0-3178c6?style=for-the-badge&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-MVP-success?style=for-the-badge&logo=rocket)

<br/>

> _"Claw your way into ML — 用爪子撕开机器学习的复杂面纱"_

<br/>

[🚀 快速开始](#-快速开始) · [📖 文档](#-架构设计) · [🎨 特性](#-核心特性) · [🛠️ 技术栈](#️-技术栈) · [🤝 贡献](#-贡献指南)

<br/>

---

</div>

## ✨ 项目一览

**NNClaw** 是一个**可视化机器学习流水线编辑器**。它将传统 ML 工作流中繁琐的代码编写，转化为**拖拽式、节点化**的操作体验。

> 🎯 **目标**：让算法工程师、ML 初学者甚至产品经理都能在浏览器中"搭"出一个完整的 ML 流水线。

| 📊 数据源 | ⚙️ 预处理 | 🧠 训练  | 📈 评估  | 🎨 可视化 |
| :-------: | :-------: | :------: | :------: | :-------: |
|   Iris    |   划分    | 随机森林 | Accuracy | 混淆矩阵  |
|   Wine    |  归一化   |   SVM    | F1 Score |  散点图   |
|  自定义   |   降维    | 逻辑回归 |   ROC    |  直方图   |
|    ...    |    ...    | XGBoost  | MAE/MSE  |    ...    |

<br/>

---

## 🎬 核心特性

<table>
<tr>
<td width="50%">

### 🎨 可视化画布编辑

- 基于 **Vue Flow** 的拖拽式节点编排
- 支持**连线、参数配置、实时预览**
- 5 种内置节点：**数据源 / 预处理 / 训练 / 评估 / 可视化**
- 节点支持自由拖拽、自定义参数

</td>
<td width="50%">

### ⚡ 一键启动全栈

- 集成 **环境自检脚本**（`scripts/check-env.cjs`）
- 自动检测 Node.js / Python / venv
- 缺失依赖**自动安装**，开箱即用
- 一条命令同时启动前后端

</td>
</tr>
<tr>
<td width="50%">

### 🔌 异步任务调度

- **FastAPI** + asyncio 后端
- 拓扑排序 + **线程池**调度
- WebSocket **实时推送**节点状态
- 支持任务取消、状态查询

</td>
<td width="50%">

### 🧩 节点可扩展

- 后端节点只需实现 `BaseExecutor`
- 前端通过 `GET /api/nodes` **自动发现**
- 解耦的 Schema 协议
- 接入 **PyTorch / XGBoost** 等新模型只需 1 个文件

</td>
</tr>
<tr>
<td width="50%">

### 📦 模型与结果管理

- 训练模型可序列化（base64 pickle）
- 评估指标结构化展示
- 混淆矩阵、特征重要性等可视化
- 训练历史快照

</td>
<td width="50%">

### 🌈 现代 UI 体验

- 暗色 / 亮色双主题
- **黄色动画连线**（`#FFD500`）
- 节点小地图、缩放控件
- 流畅的过渡与微交互

</td>
</tr>
</table>

<br/>

---

## 🏛️ 架构设计

```
┌──────────────────────────────────────────────────────────────────┐
│                   🎨  Vue 3 Frontend (Vue Flow)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ 节点面板  │  │ 画布编辑  │  │ 运行监控  │  │ 结果展示  │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
│         │             │             │             │              │
│         └─────────────┴──────┬──────┴─────────────┘              │
│                              │                                   │
│         HTTP REST (提交/查询) + WebSocket (进度推送)             │
└──────────────────────────────┼───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│              🐍  Python FastAPI Service (一体化)                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐      │
│  │  REST API  │  │ 调度引擎    │  │ 节点执行器              │      │
│  │  /api/...  │  │ 拓扑排序    │  │ ├ 数据源 (sklearn)     │      │
│  │  /ws/...   │  │ 异步调度    │  │ ├ 预处理 (split)       │      │
│  └────────────┘  │ 任务状态    │  │ ├ 训练 (RF/SVM/...)    │      │
│                  └────────────┘  │ ├ 评估 (accuracy/f1)   │      │
│                                  │ └ 可视化 (matplotlib)  │      │
│                                  └────────────────────────┘      │
│                                              │                    │
│                                              ▼                    │
│                                  ┌────────────────────┐           │
│                                  │  📚  ML 库          │           │
│                                  │  scikit-learn       │           │
│                                  │  PyTorch (可选)     │           │
│                                  │  pandas/numpy       │           │
│                                  │  matplotlib         │           │
│                                  └────────────────────┘           │
└──────────────────────────────────────────────────────────────────┘
```

> 💡 详细设计见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

<br/>

---

## 🛠️ 技术栈

### 🎨 Frontend

| 技术                                                                                           | 版本  | 用途                  |
| :--------------------------------------------------------------------------------------------- | :---: | :-------------------- |
| ![Vue](https://img.shields.io/badge/-Vue-42b883?logo=vue.js&logoColor=white)                   | 3.5+  | 渐进式前端框架        |
| ![TypeScript](https://img.shields.io/badge/-TypeScript-3178c6?logo=typescript&logoColor=white) | 6.0+  | 类型安全的 JavaScript |
| ![Vue Flow](https://img.shields.io/badge/-Vue_Flow-1.48-blue)                                  | 1.48+ | 节点画布引擎          |
| ![Vite](https://img.shields.io/badge/-Vite-8.0-646cff?logo=vite&logoColor=white)               | 8.0+  | 构建工具              |
| ![Pinia](https://img.shields.io/badge/-Pinia-3.0-yellow)                                       | 3.0+  | 状态管理              |
| ![Vue Router](https://img.shields.io/badge/-Vue_Router-5.0-4fc08d)                             | 5.0+  | 路由管理              |

### 🐍 Backend

| 技术                                                                                                  | 版本  | 用途                |
| :---------------------------------------------------------------------------------------------------- | :---: | :------------------ |
| ![Python](https://img.shields.io/badge/-Python-3776ab?logo=python&logoColor=white)                    | 3.10+ | 主语言              |
| ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?logo=fastapi&logoColor=white)                 | 最新  | 高性能异步 Web 框架 |
| ![Uvicorn](https://img.shields.io/badge/-Uvicorn-499848)                                              | 最新  | ASGI 服务器         |
| ![scikit-learn](https://img.shields.io/badge/-scikit--learn-F7931E?logo=scikit-learn&logoColor=white) | 最新  | 经典 ML 库          |
| ![PyTorch](https://img.shields.io/badge/-PyTorch-ee4c2c?logo=pytorch&logoColor=white)                 | 可选  | 深度学习            |
| ![Matplotlib](https://img.shields.io/badge/-Matplotlib-11557c)                                        | 最新  | 可视化              |

### 🔧 工具链

| 工具                | 用途                |
| :------------------ | :------------------ |
| `concurrently`      | 同时启动前后端      |
| `npm-run-all2`      | 脚本编排            |
| `oxlint` + `eslint` | 代码检查            |
| `prettier`          | 代码格式化          |
| `vue-tsc`           | TypeScript 类型检查 |

<br/>

---

## 🚀 快速开始

### 📋 环境要求

- **Node.js** `^20.19.0` 或 `>=22.12.0`
- **Python** `>= 3.10`
- **npm** / **pnpm** / \*\*yarn`

### ⚡ 一键启动（推荐）

```bash
# 克隆仓库
git clone https://github.com/DongDong1997/nnclaw.git
cd nnclaw

# 🚀 自动检查环境并启动前后端
npm run dev:all
```

> 🎉 **就这么简单！** 脚本会自动：
>
> - ✅ 检测 Node.js / npm 版本
> - ✅ 安装 `node_modules`（如缺失）
> - ✅ 创建 Python venv（如缺失）
> - ✅ 安装 Python 依赖（如缺失）
> - ✅ 同时启动前端 + 后端

### 🛠️ 分步启动

<details>
<summary><b>1️⃣ 启动后端</b></summary>

```bash
# Windows (PowerShell)
cd python_svc
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
# Linux / macOS
cd python_svc
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端将运行在：<http://localhost:8000>

API 文档（Swagger）：<http://localhost:8000/docs>

</details>

<details>
<summary><b>2️⃣ 启动前端</b></summary>

```bash
npm install
npm run dev
```

前端将运行在：<http://localhost:5173>

</details>

### 📜 可用脚本

| 命令                 | 作用                                  |
| :------------------- | :------------------------------------ |
| `npm run check`      | 🔍 仅运行环境自检（自动安装缺失依赖） |
| `npm run dev`        | 🎨 仅启动前端 Vite                    |
| `npm run dev:be`     | 🐍 仅启动后端 FastAPI                 |
| `npm run dev:all`    | ⚡ 同时启动前后端（自动先跑环境检查） |
| `npm run build`      | 📦 生产构建                           |
| `npm run type-check` | 🔬 TypeScript 类型检查                |
| `npm run lint`       | 🧹 代码风格检查                       |
| `npm run format`     | 💅 代码格式化                         |

<br/>

---

## 🎯 核心节点类型

### 📊 1. 数据源节点 `data_source`

- `sklearn.datasets.load_iris` — 经典鸢尾花
- `sklearn.datasets.load_wine` — 葡萄酒数据集
- 自定义 CSV 上传（规划中）

### ⚙️ 2. 数据预处理 `preprocess`

- 训练/测试集划分（`test_size`, `random_state`）
- 特征归一化 / 标准化
- 缺失值处理
- 类别特征编码

### 🧠 3. 模型训练 `train`

| 算法     | 参数示例                        |
| :------- | :------------------------------ |
| 随机森林 | `n_estimators`, `max_depth`     |
| SVM      | `kernel`, `C`                   |
| 逻辑回归 | `penalty`, `solver`             |
| KNN      | `n_neighbors`                   |
| XGBoost  | `learning_rate`, `n_estimators` |

### 📈 4. 模型评估 `evaluate`

- Accuracy（准确率）
- Precision / Recall
- F1 Score
- MAE / MSE / RMSE
- R² Score

### 🎨 5. 可视化 `visualize`

- 混淆矩阵
- ROC 曲线
- 特征重要性
- 训练曲线（loss/accuracy）
- 预测散点图

<br/>

---

## 🔌 API 端点

| 端点                     |  方法  | 说明                    |
| :----------------------- | :----: | :---------------------- |
| `/`                      | `GET`  | 服务信息 + 可用节点类型 |
| `/api/health`            | `GET`  | 健康检查                |
| `/api/nodes`             | `GET`  | 列出所有节点 schema     |
| `/api/workflows/run`     | `POST` | 提交工作流执行          |
| `/api/tasks/{id}`        | `GET`  | 查询任务状态            |
| `/api/tasks/{id}/cancel` | `POST` | 取消任务                |
| `/api/nodes/execute`     | `POST` | 单节点执行（调试）      |
| `/ws/tasks/{id}`         |  `WS`  | 实时任务进度推送        |

<br/>

---

## 🧩 自定义节点

### 1️⃣ 后端：实现 `BaseExecutor`

```python
# python_svc/app/executors/my_executor.py
from app.executors.base import BaseExecutor

class MyExecutor(BaseExecutor):
    def execute(self, params, inputs):
        # 你的业务逻辑
        return {"output_key": result}

    def get_schema(self):
        return {
            "type": "my_node",
            "label": "我的节点",
            "params": {
                "param_a": {"type": "number", "default": 0.5}
            },
            "inputs": ["X_train", "y_train"],
            "outputs": ["model"]
        }
```

### 2️⃣ 注册节点

```python
# python_svc/app/main.py
from app.executors.my_executor import MyExecutor
registry.register('my_node', MyExecutor())
```

### 3️⃣ 前端自动发现 ✨

无需任何代码，前端调用 `GET /api/nodes` 自动加载新节点！

<br/>

---

## 📁 项目结构

```
nnclaw/
├── 📂 src/                          # 🎨 Vue 前端
│   ├── 📂 api/
│   │   └── pythonService.ts         # Python API 客户端
│   ├── 📂 router/
│   │   └── index.ts
│   ├── 📂 views/
│   │   ├── HomeView.vue             # 主页
│   │   ├── WorkflowView.vue
│   │   └── 📂 editor/
│   │       ├── WorkflowEditor.vue   # 画布主体
│   │       └── 📂 nodes/            # 自定义节点
│   │           ├── BaseNode.vue
│   │           ├── DataSourceNode.vue
│   │           ├── PreprocessNode.vue
│   │           ├── TrainNode.vue
│   │           ├── EvaluateNode.vue
│   │           └── VisualizeNode.vue
│   ├── App.vue
│   └── main.ts
│
├── 📂 python_svc/                   # 🐍 Python FastAPI 服务
│   ├── 📂 app/
│   │   ├── main.py                  # FastAPI + 调度引擎
│   │   └── 📂 executors/            # 节点执行器
│   │       ├── base.py
│   │       ├── data_source.py
│   │       ├── preprocess.py
│   │       ├── train.py
│   │       ├── evaluate.py
│   │       └── visualize.py
│   ├── requirements.txt
│   └── pyproject.toml
│
├── 📂 docs/
│   └── ARCHITECTURE.md              # 📖 架构设计文档
│
├── 📂 scripts/
│   └── check-env.cjs                # 🔍 环境自检脚本
│
└── README.md
```

<br/>

---

## 🗺️ 路线图

|  阶段  | 内容                                                    | 状态 |
| :----: | :------------------------------------------------------ | :--: |
| **M0** | UI 框架搭建                                             |  ✅  |
| **M1** | Vue Flow 集成，画布可编辑                               |  ✅  |
| **M2** | Python FastAPI 服务骨架                                 |  ✅  |
| **M3** | 5 类基础节点 (data/preprocess/train/evaluate/visualize) |  ✅  |
| **M4** | WebSocket 实时进度推送                                  |  ✅  |
| **M5** | 结果可视化展示                                          |  ✅  |
| **M6** | 🔜 PyTorch / XGBoost 等更多模型                         |  🚧  |
| **M7** | 🔜 异步任务队列（Celery/Redis）                         |  📅  |
| **M8** | 🔜 工作流模板市场                                       |  📅  |
| **M9** | 🔜 团队协作 & 云端部署                                  |  💭  |

<br/>

---

## 📸 界面预览

> 🎨 下面是一组典型画布工作流（可在此处替换为真实截图）

```
┌─────────────────────────────────────────────────────────────┐
│  ⚡ NNClaw                                  [登录] [开始]  │
├─────────────────────────────────────────────────────────────┤
│  ┌──────┐     ┌──────┐     ┌──────┐     ┌──────┐  ┌──────┐│
│  │ 📊  │ ──→ │ ⚙️  │ ──→ │ 🧠  │ ──→ │ 📈  │  │ 🎨  ││
│  │数据源│     │ 划分 │     │ 训练 │     │ 评估 │  │可视化││
│  │      │     │      │     │      │     │      │  │      ││
│  │ Iris │     │ 0.2  │     │  RF  │     │ Acc  │  │ CM   ││
│  └──────┘     └──────┘     └──────┘     └──────┘  └──────┘│
│      💛 动画连线   💛 动画连线   💛 动画连线                │
└─────────────────────────────────────────────────────────────┘
```

<br/>

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！💖

### 🐛 报告 Bug

在 [Issues](https://github.com/DongDong1997/nnclaw/issues) 中提交，附上：

- 复现步骤
- 期望行为
- 实际行为
- 截图 / 日志

### ✨ 提交功能

1. 🍴 Fork 仓库
2. 🌿 创建特性分支（`git checkout -b feature/AmazingFeature`）
3. 💾 提交修改（`git commit -m 'feat: add amazing feature'`）
4. 📤 推送到分支（`git push origin feature/AmazingFeature`）
5. 🔃 提交 Pull Request

### 📝 代码规范

- 前端：Vue 3 Composition API + `<script setup>` + TypeScript
- 后端：PEP 8 + 类型注解
- 提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/)

<br/>

---

## 🌟 Star History

<a href="https://star-history.com/#DongDong1997/nnclaw">
  <img src="https://api.star-history.com/svg?repos=DongDong1997/nnclaw&type=Date" alt="Star History Chart" />
</a>

<br/>

---

## 📜 开源协议

本项目基于 **MIT License** 开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

<br/>

---

## 💖 致谢

- 🎨 [Vue Flow](https://vueflow.dev/) — 强大的节点画布库
- ⚡ [FastAPI](https://fastapi.tiangolo.com/) — 现代化 Python Web 框架
- 🧠 [scikit-learn](https://scikit-learn.org/) — 经典 ML 工具箱
- 💛 灵感来自 [Kaggle](https://www.kaggle.com/) / [MLflow](https://mlflow.org/) / [Apache Airflow](https://airflow.apache.org/)

<br/>

---

<div align="center">

### ⭐ 如果这个项目对你有帮助，请给个 Star

<br/>

**Made with 💛 by NNClaw Team**

<br/>

[⬆ 回到顶部](#-nnclaw)

</div>
