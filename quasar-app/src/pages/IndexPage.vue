<template>
  <q-page>
    <div class="row full-width q-mt-xl">
      <div class="col-2"></div>
      <div class="col row items-center justify-center">
        <div class="text-h6 q-mb-md">
          The Midnight Times - A Place to find the latest news
        </div>
        <q-input
          outlined
          label="Search"
          @keyup.enter.prevent="searchNews"
          v-model.trim="search"
          debounce="1000"
          style="width: 40rem"
          rounded
        >
          <template v-slot:append>
            <q-icon name="search" style="cursor: pointer" @click="searchNews" />
          </template>
        </q-input>
      </div>
      <div class="col-2"></div>
    </div>
    <div class="flex q-pa-md" v-show="previous_searches.length > 0">
      <q-separator />
      <div class="row full-width text-subtitle1 text-grey-8">
        Previous searches, click to view
      </div>
      <div class="row">
        <q-btn
          v-for="(item, idx) in previous_searches"
          :key="idx + 1"
          rounded
          no-caps
          class="q-mr-sm q-mt-sm bg-grey text-white"
          flat
          style="cursor: pointer"
          @click="visitSearch(item)"
        >
          {{ item.key_phrase }}
        </q-btn>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { QSpinnerGears } from "quasar";

export default defineComponent({
  name: "IndexPage",
  data() {
    return {
      search: "",
      previous_searches: [],
    };
  },

  methods: {
    visitSearch(item) {
      let self = this;
      self.$router.push({
        path: "/results",
        query: { past_search: item.key_phrase },
      });
    },
    searchNews() {
      let self = this;
      self.$router.push({ path: "/results", query: { search: self.search } });
    },
    previousSearches() {
      let self = this;
      self.$q.loading.show({
        spinner: QSpinnerGears,
        message: "Loading Previous Searches...",
      });
      self.$axios
        .get("/api/news/")
        .then(function (response) {
          if (response.data.success) {
            self.previous_searches = response.data.data;
          }
          self.$q.loading.hide();
        })
        .catch(function (error) {
          self.$q.loading.hide();
          self.$q.notify({
            color: "red-5",
            textColor: "white",
            icon: "warning",
            message: error.response.data.detail,
          });
        });
    },
  },

  created() {
    let self = this;
    self.previousSearches();
  },
});
</script>
