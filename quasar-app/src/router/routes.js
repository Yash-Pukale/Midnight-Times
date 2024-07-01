const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue'), name: 'home' },
      { path: '/results', component: () => import('pages/NewsResults.vue'), name: 'results' },
      { path: '/admin/users', component: () => import('pages/AdminListUsers.vue'), name: 'users' },
    ]
  },
  {
    path: '/sign-in',
    component: () => import('pages/LoginPage.vue'),
    name: 'sign-in'
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
