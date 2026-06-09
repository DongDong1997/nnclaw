import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../HomeView.vue'
import WorkflowView from '../views/WorkflowView.vue'
import WorkflowEditor from '../views/editor/WorkflowEditor.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/workflow',
      name: 'workflow',
      component: WorkflowView,
    },
    {
      path: '/editor',
      name: 'editor',
      component: WorkflowEditor,
    },
  ],
})

export default router
