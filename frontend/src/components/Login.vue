<template>
  <v-container>
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
  </v-container>
</template>

<script>
  export default {
    name: 'Login',

    data: () => ({
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

        this.$http.post('http://localhost:5000/api/login', {
          mail: this.email,
          password: this.password
        })
        .then(response => {
          console.log(response.body);
          this.$cookies.set('Authorization', 'Bearer ' + response.body['session'], '1d');
          // redirect to profile
        }, response => {
          console.log(response.body);
        });
      },

      checkAuth: function() {
        this.$http.get('http://localhost:5000/api/login', {
          headers: {'Authorization': this.$cookies.get('Authorization')}
        })
        .then(response => {
          console.log(response.body);
          return true;
        });

        return false;
      }
    }
  }
</script>
