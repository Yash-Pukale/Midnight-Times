<template>
  <q-page>
    <div class="flex justify-between full-width q-pa-md">
      <div class="row">
        <div class="col q-mt-md text-h6">
          Searched Results For: {{ searched_value }}
        </div>
      </div>
      <div class="row">
        <q-input
          outlined
          label="Search More..."
          @keyup.enter.prevent="searchNews"
          v-model.trim="search"
          debounce="1000"
          style="width: 30rem"
          class="q-mr-sm"
          rounded
          dense
        >
          <template v-slot:append>
            <q-icon name="search" style="cursor: pointer" />
          </template>
        </q-input>
        <q-btn
          rounded
          size="sm"
          color="primary"
          icon="refresh"
          @click="fetchLatestNews"
        >
          <q-tooltip>Refresh Results</q-tooltip>
        </q-btn>
      </div>
    </div>
    <q-separator />
    <div class="flex full-width q-pa-md bg-grey-2">
      <q-list separator class="bg-white">
        <q-item
          v-for="(item, idx) in news"
          :key="idx"
          clickable
          :href="item.url"
          target="_blank"
        >
          <q-item-section top thumbnail class="q-ml-none">
            <img :src="item.urlToImage" alt="No Image" />
          </q-item-section>
          <q-item-section>
            <q-item-label
              >{{ item.title
              }}<span class="text-grey" style="font-size: 10px">
                ({{ item.source?.name || "Unknown Source" }})</span
              ></q-item-label
            >
            <q-item-label caption>{{ item.description }}</q-item-label>
          </q-item-section>
          <q-item-section side top>
            <q-badge color="amber-2" class="text-black">{{
              item.publishedAt
            }}</q-badge>
          </q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { QSpinnerGears } from "quasar";

export default defineComponent({
  name: "NewsResults",
  data() {
    return {
      search: "",
      searched_value: "",
      news: [],
      search_type: "new",
    };
  },

  methods: {
    fetchLatestNews() {
      self.search_type = "latest";
      self.searchNews();
    },
    searchNews() {
      let self = this;
      self.$q.loading.show({
        spinner: QSpinnerGears,
        message: "Please wait...",
      });
      self.$axios
        .post("/api/news/", {
          key_phrase: self.search,
          search_type: self.search_type,
        })
        .then(function (response) {
          if (response.data.success) {
            self.news = response.data.data.articles;
            self.searched_value = self.search;
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
    self.search = self.$route.query.search;
    if (self.search) {
      self.search_type = "new";
      self.searchNews();
    } else if (self.$route.query.past_search) {
      self.search_type = "past";
      self.search = self.$route.query.past_search;
      self.searchNews();
    }
  },
});
</script>
