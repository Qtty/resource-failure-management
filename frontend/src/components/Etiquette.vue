<template>
  <v-card
    class="mx-auto my-6"
    max-width="396"
    max-height="158"
    outlined
  >
    <v-list-item
    three-line
    v-if="!error.exists"
    >
      <v-list-item-content>
        <v-list-item-title class="text-h5 mb-1">
          Flashez-Moi!
        </v-list-item-title>
        <v-list-item-subtitle>{{ etiquette.description }} - {{ etiquette.localisation }}</v-list-item-subtitle>
      </v-list-item-content>

      <v-list-item-avatar
        tile
        size="100"
      >
        <v-img :src="etiquette.qrcode_url"></v-img>
      </v-list-item-avatar>
    </v-list-item>

    <v-list-item
    v-else
    >
          {{ error.text }}
    </v-list-item>

    <div
    class="mx-2"
    id="url"
    >
        {{ etiquette.url }}
    </div>

  </v-card>
</template>

<script>
export default {
    name: "Etiquette",

    data: () => ({
        etiquette: {url: '', qrcode_url: '', description: '', localisation: ''},
        error: {exists: true, text: ''}
    }),
    methods: {
        getEtiq: function() {
            this.$http.post(`${this.$api}/responsable`, {
              _id: this.$route.params._id,
              url: window.location.origin
              }, {
                headers: {'Authorization': this.$cookies.get('Authorization')},
            })
            .then(response => {
              this.error.exists = false;
              this.etiquette.qrcode_url = `${window.location.origin}/api/qrcodes/${this.$route.params._id}.png`;
              this.etiquette.url = response.body.url;
              this.etiquette.description = response.body.description;
              this.etiquette.localisation = response.body.localisation;
            }, response => {
              console.log(response);
              if (response.status == 401)
                this.$router.push('/login');
              else {
                this.error.exists = true;
                this.error.text = response.body;
              }
            });
        }
    },
    created() {
        this.getEtiq();
    }
}
</script>

<style lang="css">
    #url {
        font-size: 00.8em;
    }
</style>