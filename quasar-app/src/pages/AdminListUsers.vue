<template>
  <q-page>
    <div class="row q-gutter-sm q-px-sm q-pt-md q-pb-none">
      <div class="col">
        <div
          style="
            background: rgb(241, 163, 118);
            background: linear-gradient(
              90deg,
              rgba(241, 163, 118, 1) 15%,
              rgba(242, 125, 147, 1) 100%
            );
          "
          class="tw-border border-gray-200 tw-rounded-md tw-overflow-hidden tw-cursor-pointer"
        >
          <div class="tw-flex row text-white tw-relative">
            <div
              class="tw-px-4 flex flex-wrap justify-between tw-pt-4 tw-pb-3 col-9"
            >
              <div class="tw-text-xl">Users Onboarded Till Date</div>
              <div
                class="tw-w-full tw-flex-none tw-text-4xl tw-font-medium tw-mt-2 tw-leading-10 tw-tracking-tight"
              >
                {{ users.length }}
              </div>
              <div class="" style="font-size: 0.75rem"></div>
              <div class="tw-absolute tw-right-0 tw-top-0">
                <img
                  src="~assets/dashboard_one.svg"
                  alt="Model Image"
                  style="height: 76px"
                  class="tw-float-right"
                />
              </div>
              <div
                class="tw-absolute tw-right-0 tw-bottom-0"
                style="margin-bottom: -34px"
              >
                <img
                  src="~assets/dashboard_two.svg"
                  alt="Model Image"
                  style="height: 76px"
                  class="tw-float-right"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col">
        <div
          style="
            background: rgb(199, 174, 250);
            background: linear-gradient(
              90deg,
              rgba(199, 174, 250, 1) 15%,
              rgba(130, 154, 246, 1) 100%
            );
          "
          class="tw-border border-gray-200 tw-rounded-md tw-cursor-pointer"
        >
          <div class="text-white tw-relative">
            <div class="tw-px-4 tw-pt-4 tw-pb-3">
              <div class="row tw-text-xl">Top Searches By Users</div>
              <div class="row q-pt-lg full-width">
                <div
                  class="col-4 tw-text-md"
                  v-for="(key, idx) in top_searches"
                  :key="idx"
                >
                  {{ idx + 1 }}. {{ key.key_phrase }}
                  <q-icon
                    size="sm"
                    name="workspace_premium"
                    :color="
                      idx === 0 ? 'yellow-6' : idx === 1 ? 'grey-4' : 'brown-7'
                    "
                  ></q-icon>
                </div>
              </div>

              <div class="tw-absolute tw-right-0 tw-top-0">
                <img
                  src="~assets/dashboard_one.svg"
                  alt="Model Image"
                  style="height: 76px"
                  class="tw-float-right"
                />
              </div>
              <div
                class="tw-absolute tw-right-0 tw-bottom-0"
                style="margin-bottom: -34px"
              >
                <img
                  src="~assets/dashboard_two.svg"
                  alt="Model Image"
                  style="height: 76px"
                  class="tw-float-right"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row full-width q-px-sm q-pt-none">
      <q-table
        class="full-width"
        flat
        title="Users"
        :rows="users"
        :columns="user_columns"
        :filter="filter"
        row-key="id"
        virtual-scroll
      >
        <template v-slot:top-right>
          <q-input
            outlined
            dense
            debounce="300"
            v-model="filter"
            placeholder="Search"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </template>
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
              v-show="col.name !== 'is_active'"
            >
              {{ col.label }}
            </q-th>
            <q-th :props="props" key="is_active">
              {{ props.cols[props.cols.length - 1].label }}
              <span>
                <q-icon name="info" color="primary" size="xs">
                  <q-tooltip
                    >You can mark any user as Active or Inactive except
                    Admins</q-tooltip
                  >
                </q-icon>
              </span>
            </q-th>
          </q-tr>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td key="id" :props="props"> #{{ props.row.id }} </q-td>
            <q-td key="first_name" :props="props">
              {{ props.row.first_name || "NA" }}
            </q-td>
            <q-td key="last_name" :props="props">
              {{ props.row.last_name || "NA" }}
            </q-td>
            <q-td key="email" :props="props">
              {{ props.row.email }}
            </q-td>
            <q-td key="date_joined" :props="props">
              {{ props.row.date_joined }}
            </q-td>
            <q-td key="is_superuser" :props="props">
              <q-icon
                size="sm"
                :name="props.row.is_superuser ? 'check_circle' : 'cancel'"
                :color="props.row.is_superuser ? 'green' : 'red'"
              />
            </q-td>
            <q-td key="is_active" :props="props">
              <q-btn
                :disabled="props.row.is_superuser"
                @click="toggleUserStatus(props.row)"
                size="sm"
                dense
                no-caps
                :color="props.row.is_active ? 'green' : 'red'"
                :label="props.row.is_active ? 'Active' : 'Inactive'"
              />
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { QSpinnerGears } from "quasar";

export default defineComponent({
  name: "AdminListUsers",
  data() {
    return {
      users: [],
      top_searches: [],
      filter: "",
      user_columns: [
        {
          name: "id",
          required: true,
          label: "User ID",
          align: "left",
          field: (row) => row.id,
          format: (val) => `${val}`,
          sortable: true,
          headerStyle: "background-color: #dbd8d8;",
        },
        {
          name: "first_name",
          required: true,
          label: "First Name",
          align: "left",
          field: (row) => row.first_name,
          format: (val) => `${val}` || "NA",
          sortable: true,
          headerStyle: "background-color: #dbd8d8;",
        },
        {
          name: "last_name",
          required: true,
          label: "Last Name",
          align: "left",
          field: (row) => row.last_name,
          format: (val) => `${val}` || "NA",
          sortable: true,
          headerStyle: "background-color: #dbd8d8;",
        },
        {
          name: "email",
          required: true,
          label: "Email ID",
          align: "left",
          field: (row) => row.email,
          format: (val) => `${val}`,
          sortable: true,
          headerStyle: "background-color: #dbd8d8;",
        },
        {
          name: "date_joined",
          required: true,
          label: "Joined On",
          align: "left",
          field: (row) => row.date_joined,
          format: (val) => `${val}`,
          sortable: true,
          headerStyle: "background-color: #dbd8d8;",
        },
        {
          name: "is_superuser",
          required: true,
          label: "Is Admin",
          align: "center",
          field: (row) => row.is_superuser,
          format: (val) => `${val}`,
          sortable: true,
          headerStyle: "background-color: #dbd8d8;",
        },
        {
          name: "is_active",
          required: true,
          label: "Status",
          align: "center",
          field: (row) => row.is_active,
          format: (val) => `${val}`,
          sortable: true,
          headerStyle: "background-color: #dbd8d8; width: 200px;",
        },
      ],
    };
  },

  methods: {
    getUsers() {
      let self = this;
      self.$q.loading.show({
        spinner: QSpinnerGears,
        message: "Getting Users...",
      });
      self.$axios
        .get("/accounts/users/")
        .then(function (response) {
          if (response.data.success) {
            self.users = response.data.data;
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
    toggleUserStatus(user) {
      let self = this;
      let msg =
        "This is prevent user from getting logged in. Are you sure you want to mark this user as Inactive?";
      self.$q
        .dialog({
          title: "Confirm",
          message: user.is_active
            ? msg
            : "Are you sure you want to mark this user as Active?",
          cancel: true,
          persistent: true,
        })
        .onOk(() => {
          self.$q.loading.show({
            spinner: QSpinnerGears,
            message: "Updating User...",
          });
          self.$axios
            .post("/accounts/mark_as_inactive/", {
              email: user.email,
              is_active: !user.is_active,
            })
            .then(function (response) {
              if (response.data.success) {
                self.getUsers();
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
        });
    },
    trendingKeyPhrases() {
      let self = this;
      self.$q.loading.show({
        spinner: QSpinnerGears,
        message: "Loading Top Searches...",
      });
      self.$axios
        .get("/api/key-phrases/")
        .then(function (response) {
          if (response.data.success) {
            self.top_searches = response.data.data;
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
    self.getUsers();
    self.trendingKeyPhrases();
  },
});
</script>
