<template>
  <div
    class="flex flex-center bg-amber-2"
    :style="{ 'min-height': dynamicHeight + 'px' }"
  >
    <div class="col"></div>
    <div class="col">
      <div class="row text-h4 q-my-md">The Midnight Times | JSE</div>
      <q-card style="max-width: 26.5rem; width: 100%">
        <q-card-section class="text-center">
          <q-tabs
            v-model="page_type"
            no-caps
            align="center"
            class="text-primary shadow-2"
          >
            <q-tab name="Login" label="Login" />
            <q-tab name="Register" label="Register" />
          </q-tabs>
        </q-card-section>
        <q-card-section class="q-pt-none" v-show="page_type === 'Login'">
          <q-input
            class="q-mt-sm"
            label="Email"
            dense
            v-model="email"
            type="text"
            outlined
          >
            <template v-slot:append>
              <q-icon name="person" size="xs" />
            </template>
          </q-input>

          <q-input
            class="q-mt-sm"
            label="Password"
            dense
            v-model="password"
            :type="is_pwd ? 'password' : 'text'"
            outlined
          >
            <template v-slot:append>
              <q-icon
                size="xs"
                :name="is_pwd ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="is_pwd = !is_pwd"
              />
            </template>
          </q-input>
        </q-card-section>
        <q-card-section v-show="page_type === 'Register'">
          <q-input
            class="q-mt-sm"
            label="First Name"
            dense
            v-model="user.first_name"
            type="text"
            outlined
          >
          </q-input>

          <q-input
            class="q-mt-sm"
            label="Last Name"
            dense
            v-model="user.last_name"
            type="text"
            outlined
          >
          </q-input>

          <q-input
            class="q-mt-sm"
            label="Email"
            dense
            v-model="user.email"
            type="text"
            outlined
          >
          </q-input>

          <q-input
            class="q-mt-sm"
            label="Password"
            dense
            v-model="user.password"
            type="password"
            outlined
          >
          </q-input>

          <q-input
            class="q-mt-sm"
            label="Confirm Password"
            dense
            v-model="temp_password"
            type="password"
            outlined
          >
          </q-input>
        </q-card-section>
        <q-card-actions align="center">
          <q-btn
            :disabled="
              page_type === 'Register' && user.password !== temp_password
            "
            style="width: 25rem"
            :label="page_type"
            color="primary"
            @click="submitted"
          ></q-btn>
        </q-card-actions>
      </q-card>
    </div>
    <div class="col"></div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { QSpinnerGears } from "quasar";

export default defineComponent({
  name: "LoginPage",
  data() {
    return {
      email: "",
      password: "",
      is_pwd: true,
      page_type: "Login",
      user: {
        first_name: "",
        last_name: "",
        email: "",
        password: "",
      },
      temp_password: "",
    };
  },
  methods: {
    submitted() {
      if (this.page_type === "Login") {
        this.login();
      } else {
        this.register();
      }
    },
    register() {
      let self = this;
      if (
        self.user.first_name.trim() === "" ||
        self.user.last_name.trim() === "" ||
        self.user.email.trim() === "" ||
        self.user.password.trim() === ""
      ) {
        self.$q.notify({
          color: "red-5",
          textColor: "white",
          icon: "warning",
          message: "All fields are required",
        });
        return;
      }
      self.$q.loading.show({
        spinner: QSpinnerGears,
        message: "Please wait...",
      });
      self.$axios
        .post("/accounts/register/", {
          first_name: self.user.first_name,
          last_name: self.user.last_name,
          email: self.user.email,
          password: self.user.password,
        })
        .then(function (response) {
          self.$q.loading.hide();
          if (response.data.success) {
            self.email = self.user.email;
            self.password = self.user.password;
            self.login();
          } else {
            self.$q.notify({
              color: "red-5",
              textColor: "white",
              icon: "warning",
              message: response.data.message,
            });
          }
        })
        .catch(function (error) {
          self.$q.loading.hide();
          self.$q.notify({
            color: "red-5",
            textColor: "white",
            icon: "warning",
            message: error.message,
          });
        });
    },

    login() {
      let self = this;
      if (self.email.trim() === "" || self.password.trim() === "") {
        self.$q.notify({
          color: "red-5",
          textColor: "white",
          icon: "warning",
          message: "Email and password are required",
        });
        return;
      }
      self.$q.loading.show({
        spinner: QSpinnerGears,
        message: "Please wait...",
      });
      self.$axios
        .post("/accounts/token/", {
          email: self.email,
          password: self.password,
        })
        .then(function (response) {
          if (response.status === 200) {
            self.$q.localStorage.set("token", response.data.access);
            self.$q.localStorage.set("refresh", response.data.refresh);
            self.$q.localStorage.set("user_logged_in", true);
            self.$q.localStorage.set("is_admin", response.data.is_admin);
            self.$q.loading.hide();
            self.$router.push("/");
          } else {
            self.$q.loading.hide();
            self.$q.notify({
              color: "red-5",
              textColor: "white",
              icon: "warning",
              message: response.data.message,
            });
          }
        })
        .catch(function (error) {
          self.$q.loading.hide();
          if (error.response.status === 401) {
            self.$q.notify({
              color: "red-5",
              textColor: "white",
              icon: "warning",
              message: error.response.data.detail,
            });
          } else {
            self.$q.notify({
              color: "red-5",
              textColor: "white",
              icon: "warning",
              message: error.message,
            });
          }
        });
    },
  },
  computed: {
    dynamicHeight() {
      return this.$q.screen.height;
    },
  },
});
</script>
