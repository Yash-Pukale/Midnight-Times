import {defineStore} from 'pinia';

export const varStore = defineStore('store_data', {
  state: () => ({
    variant_redirect_val: '',
  }),
});
