# nnclaw — Quick Look

> 📖 想要了解项目全貌、特性和架构？请查看 [README.md](README.md)

---

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

## 启动项目 (一键)

```sh
# 自动检查环境并启动前后端
npm run dev:all
```

可用脚本:

| 命令 | 作用 |
|------|------|
| `npm run check` | 仅运行环境自检(自动安装缺失依赖) |
| `npm run dev` | 仅启动前端 Vite |
| `npm run dev:be` | 仅启动后端 FastAPI |
| `npm run dev:all` | 同时启动前后端(自动先跑环境检查) |

环境自检 [scripts/check-env.cjs](file:///f:/code/ai_code/nnclaw/scripts/check-env.cjs) 会自动检测:
- Node.js / npm 版本
- `node_modules` 是否存在,缺失自动 `npm install`
- Python 版本 (>= 3.10)
- `python_svc/venv` 是否存在,缺失自动创建
- `requirements.txt` 中所有包是否已安装,缺失自动 `pip install`

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
