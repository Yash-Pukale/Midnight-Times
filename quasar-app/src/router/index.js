import { route } from 'quasar/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { LocalStorage } from 'quasar';

import {setActivePinia} from "pinia/dist/pinia";
import {createPinia} from "pinia";

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */
export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.MODE === 'ssr' ? void 0 : process.env.VUE_ROUTER_BASE)
  })

  Router.beforeEach((to, from, next) => {
    const isUserLoggedIn = LocalStorage.getItem('user_logged_in') === 'true';
    const hasToken = LocalStorage.getItem('token');
    if (isUserLoggedIn) {
      const userData = JSON.parse(LocalStorage.getItem('user_data'));
    }
    const publicPages = ['sign-in'];

    if (!isUserLoggedIn && !hasToken) {
      // Not logged in
      if (publicPages.includes(to.name) || publicPages.includes(to.path)) {
        // Allow navigation to public pages or certain routes
        next();
      } else {
        // Redirect to signup for other routes
        next('/sign-in');
      }
    } else {
      if(publicPages.includes(to.path) && to.path == "/" ){
        next()
      }
      // Logged in
      else if (!publicPages.includes(to.path)) {
        // Allow navigation to non-public pages
        next();
      } else {
        // Redirect to home for public pages or logout
        next();
      }
    }
  });
  setActivePinia(createPinia())
  return Router
})
