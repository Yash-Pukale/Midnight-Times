<template>
  <q-layout view="hHh lpR fFf" class="">
    <q-header elevated class="bg-amber-2 text-black">
      <q-toolbar>
        <q-toolbar-title @click="$router.push('/')" style="cursor: pointer">
          The Midnight Times | JSE
        </q-toolbar-title>
        <q-btn
          v-if="is_admin && !$route.path.includes('admin')"
          label="Admin Panel"
          icon="manage_accounts"
          class="float-right q-mr-sm bg-primary text-white"
          dense
          no-caps
          @click="$router.push('/admin/users')"
        >
        </q-btn>
        <q-btn
          label="Sign Out"
          class="float-right bg-primary text-white"
          dense
          no-caps
          icon="exit_to_app"
          @click="logout"
        >
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="drawer"
      show-if-above
      v-if="is_admin && $route.path.includes('admin')"
      :mini="miniState"
      @mouseover="miniState = false"
      @mouseout="miniState = true"
      :width="200"
      :breakpoint="500"
      bordered
      :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-3'"
    >
      <q-scroll-area class="fit" :horizontal-thumb-style="{ opacity: 0 }">
        <q-list padding>
          <q-item
            :active="$route.path === '/admin/users'"
            clickable
            v-ripple
            @click="$router.push('/admin/users')"
          >
            <q-item-section avatar>
              <q-icon name="group" />
            </q-item-section>
            <q-item-section> Users </q-item-section>
          </q-item>
          <q-separator />
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  data() {
    return {
      left: true,
      miniState: true,
      drawer: true,
      is_admin: false,
    };
  },
  methods: {
    logout() {
      this.$q.localStorage.remove();
      this.$router.push("/sign-in");
    },
  },
  created() {
    this.$q.localStorage.has("is_admin")
      ? (this.is_admin = this.$q.localStorage.getItem("is_admin"))
      : (this.is_admin = false);
  },
};
</script>
<style></style>
