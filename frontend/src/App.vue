<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Univ Logo"
          class="shrink mr-2"
          contain
          :src="require('./assets/univ-logo.png')"
          transition="scale-transition"
          width="120"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
      @click="removeAuth"
      icon
      v-show="show_logout"
      >
        <v-icon>mdi-logout</v-icon>
      </v-btn>

    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  components: {
  },

  data: () => ({
    //
  }),
  methods: {
    removeAuth: function() {
      this.$cookies.remove('Authorization');
      this.$is_logged = false;
    }
  },
  computed: {
    show_logout: function() {
      console.log(this.$is_logged);
      return this.$is_logged;
    }
  }
};
</script>
