<template>
  <v-container 
  class="d-flex"
  v-if="!is_auth"
  >
    <v-card
    class="flex-grow-1 flex-shrink-0 ma-auto pa-4"
    max-width="60%"
    >
      <v-card-title class="justify-center">Login</v-card-title>

      <v-divider></v-divider>

      <v-form
        ref="form"
        v-model="valid"
        lazy-validation
      >

        <v-text-field
          v-model="email"
          :rules="emailRules"
          label="E-mail"
          required
        ></v-text-field>

        <v-text-field
          v-model="password"
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="passwordRules"
          :type="show ? 'text' : 'password'"
          label="Password"
          @click:append="show = !show"
        ></v-text-field>

        <v-btn
          :disabled="!valid"
          color="success"
          class="mr-4"
          @click="validate"
        >
          Validate
        </v-btn>

        <v-btn
          color="success"
          class="mr-4"
          @click="checkAuth"
        >
          Check Auth
        </v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
  export default {
    name: 'Login',

    data: () => ({
      is_auth: false,
      valid: true,
      show: false,
      email: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
      password: '',
      passwordRules: [
        v => !!v || 'Password is required',
      ]
    }),
    methods: {
      validate: function() {
        this.$refs.form.validate();

        this.$http.post(`${this.$api}/login`, {
          mail: this.email,
          password: this.password
        })
        .then(response => {
          console.log(response.body);
          this.$cookies.set('Authorization', 'Bearer ' + response.body['session'], '1d');
          this.is_auth = true;
          this.checkAuth();
        }, response => {
          this.is_auth = false;
          console.log(response.body);
        });

      },

      checkAuth: function() {
        this.$http.get(`${this.$api}/login`, {
          headers: {'Authorization': this.$cookies.get('Authorization')}
        })
        .then(response => {
          console.log(response.body);
          this.is_auth = true;
          if (response.body.is_admin)
            this.$router.push("admin");
          else
            this.$router.push("profile");

        }, () => {
          this.is_auth = false;
        });
      }
    },
    created() {
      this.checkAuth();
    }
  }
</script>
