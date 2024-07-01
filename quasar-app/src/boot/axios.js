import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({ baseURL: process.env.APP_BASE_URL, withCredentials: true })

export default boot(({ app, router, store }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api
  api.interceptors.request.use(function (config) {
    // config.headers.post['Content-Type'] = 'application/json';
    // config.headers.delete['Content-Type'] = 'application/json';
    const accessToken = localStorage.getItem('token');
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken.replace('__q_strn|','')}`;
    }
    return config;
  });
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file
  api.interceptors.response.use(
    (response) => {
      return response;
    }),
    async (error) => {
      if (error.response.status === 401) {
        router.replace('/login');
        return new Promise(() => {
        });
      } else {
        return Promise.reject(error);
      }
    }

  app.config.globalProperties.$axios = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

export { api }
