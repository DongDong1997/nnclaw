#!/usr/bin/env node
/**
 * NNClaw 环境自检脚本
 *
 * 功能:
 *   1. 检测 Node.js / npm 版本
 *   2. 检测 node_modules,缺失则自动 npm install
 *   3. 检测 Python 与 venv
 *   4. 检测 Python 依赖包,缺失则自动 pip install
 *
 * 用法:
 *   node scripts/check-env.js
 *   npm run check
 */

const { execSync, spawnSync } = require('node:child_process')
const fs = require('node:fs')
const path = require('node:path')
const os = require('node:os')

const ROOT = path.resolve(__dirname, '..')
const PY_SVC = path.join(ROOT, 'python_svc')

const isWin = os.platform() === 'win32'
const VENV_PATH = path.join(PY_SVC, 'venv')
const VENV_PYTHON = isWin
  ? path.join(VENV_PATH, 'Scripts', 'python.exe')
  : path.join(VENV_PATH, 'bin', 'python')
const VENV_PIP = isWin
  ? path.join(VENV_PATH, 'Scripts', 'pip.exe')
  : path.join(VENV_PATH, 'bin', 'pip')

// ============ 工具函数 ============

const c = {
  red: (s) => `\x1b[31m${s}\x1b[0m`,
  green: (s) => `\x1b[32m${s}\x1b[0m`,
  yellow: (s) => `\x1b[33m${s}\x1b[0m`,
  cyan: (s) => `\x1b[36m${s}\x1b[0m`,
  bold: (s) => `\x1b[1m${s}\x1b[0m`,
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
}

function log(icon, msg, color = 'cyan') {
  console.log(`${c[color](icon)} ${msg}`)
}

function step(title) {
  console.log('\n' + c.bold(c.cyan(`━━━ ${title} ━━━`)))
}

function ok(msg) {
  log('✓', msg, 'green')
}
function warn(msg) {
  log('!', msg, 'yellow')
}
function fail(msg) {
  log('✗', msg, 'red')
}

function run(cmd, opts = {}) {
  try {
    return execSync(cmd, { stdio: 'pipe', encoding: 'utf-8', ...opts })
  } catch (e) {
    return null
  }
}

function parseVersion(v) {
  const m = (v || '').match(/(\d+)\.(\d+)\.(\d+)/)
  return m ? [+m[1], +m[2], +m[3]] : [0, 0, 0]
}

function cmpVer(a, b) {
  for (let i = 0; i < 3; i++) {
    if (a[i] > b[i]) return 1
    if (a[i] < b[i]) return -1
  }
  return 0
}

const problems = []

// ============ 1. Node.js 检查 ============

step('1/4  检查 Node.js 与 npm')

const nodeVer = parseVersion(process.version)
if (cmpVer(nodeVer, [20, 19, 0]) < 0 && cmpVer(nodeVer, [22, 12, 0]) < 0) {
  fail(`Node.js 版本过低: ${process.version} (需要 >= 20.19.0 或 >= 22.12.0)`)
  problems.push('node')
} else {
  ok(`Node.js ${process.version}`)
}

const npmVer = run('npm --version')
if (npmVer) {
  ok(`npm ${npmVer.trim()}`)
} else {
  fail('npm 未安装')
  problems.push('npm')
}

// ============ 2. node_modules 检查 ============

step('2/4  检查前端依赖 (node_modules)')

const nodeModules = path.join(ROOT, 'node_modules')
if (!fs.existsSync(nodeModules)) {
  warn('node_modules 缺失,正在自动安装...')
  console.log(c.dim('  $ npm install'))
  const result = spawnSync('npm', ['install'], {
    cwd: ROOT,
    stdio: 'inherit',
    shell: true,
  })
  if (result.status === 0) {
    ok('前端依赖安装完成')
  } else {
    fail('前端依赖安装失败')
    problems.push('npm-install')
  }
} else {
  ok('node_modules 已存在')
}

// ============ 3. Python 检查 ============

step('3/4  检查 Python 环境')

// 尝试多个 python 命令
let pyCmd = null
let pyVer = null
for (const cmd of ['python', 'python3', 'py']) {
  const out = run(`${cmd} --version`)
  if (out && out.toLowerCase().includes('python')) {
    pyCmd = cmd
    pyVer = parseVersion(out)
    break
  }
}

if (!pyCmd) {
  fail('未检测到 Python,请先安装 Python 3.10+')
  problems.push('python')
} else if (cmpVer(pyVer, [3, 10, 0]) < 0) {
  fail(`Python 版本过低: ${pyVer.join('.')} (需要 >= 3.10)`)
  problems.push('python-version')
} else {
  ok(`Python ${pyVer.join('.')} (${pyCmd})`)
}

// ============ 4. venv 检查 ============

step('4/4  检查 Python 虚拟环境与依赖')

if (!fs.existsSync(VENV_PYTHON)) {
  warn(`venv 缺失,正在创建: ${VENV_PATH}`)
  console.log(c.dim(`  $ ${pyCmd} -m venv "${VENV_PATH}"`))
  const result = spawnSync(pyCmd, ['-m', 'venv', VENV_PATH], {
    stdio: 'inherit',
    shell: true,
  })
  if (result.status !== 0) {
    fail('venv 创建失败')
    problems.push('venv')
  } else {
    ok('venv 创建完成')
  }
} else {
  ok(`venv 已存在 (${VENV_PATH})`)
}

// 检查 requirements.txt
const reqFile = path.join(PY_SVC, 'requirements.txt')
if (!fs.existsSync(reqFile)) {
  warn('requirements.txt 未找到')
} else {
  const reqs = fs
    .readFileSync(reqFile, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith('#') && !l.startsWith('-'))

  if (reqs.length === 0) {
    ok('requirements.txt 为空')
  } else {
    // 检查每个包是否已安装
    const missing = []
    for (const pkg of reqs) {
      const pkgName = pkg.split(/[=<>~!]/)[0].trim()
      if (!pkgName) continue
      const check = run(
        `"${VENV_PYTHON}" -c "import importlib; importlib.import_module('${pkgName.replace(/-/g, '_')}')"`,
      )
      if (check === null) missing.push(pkg)
    }

    if (missing.length === 0) {
      ok(`所有 ${reqs.length} 个 Python 依赖已安装`)
    } else {
      warn(`缺失 ${missing.length} 个 Python 依赖,正在安装...`)
      console.log(c.dim(`  $ "${VENV_PIP}" install -r "${reqFile}"`))
      const result = spawnSync(VENV_PIP, ['install', '-r', reqFile], {
        stdio: 'inherit',
        shell: true,
      })
      if (result.status === 0) {
        ok('Python 依赖安装完成')
      } else {
        fail('Python 依赖安装失败')
        problems.push('pip-install')
      }
    }
  }
}

// ============ 总结 ============

console.log('\n' + '━'.repeat(50))
if (problems.length === 0) {
  console.log(c.bold(c.green('✓ 环境检查通过,可以启动项目了!')))
  console.log(c.dim('  运行: npm run dev:all'))
  process.exit(0)
} else {
  console.log(c.bold(c.red('✗ 环境存在问题,请先解决:')))
  problems.forEach((p) => console.log(`  - ${c.red(p)}`))
  console.log()
  console.log(c.dim('常见解决方案:'))
  console.log(c.dim('  • 安装 Node.js: https://nodejs.org/'))
  console.log(c.dim('  • 安装 Python: https://www.python.org/downloads/'))
  console.log(c.dim('  • 手动安装前端依赖: npm install'))
  console.log(c.dim('  • 手动安装后端依赖: cd python_svc && venv\\Scripts\\activate && pip install -r requirements.txt'))
  process.exit(1)
}
