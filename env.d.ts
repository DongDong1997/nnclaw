/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_PYTHON_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
