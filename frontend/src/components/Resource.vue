<template>
    <v-container class="d-flex">
        <v-col>
            <v-row
            class="mb-5"
            >
                <v-card
                    class="pa-1"
                    max-width="20%"
                    tile
                >
                    <v-list shaped>
                        <v-list-item-group
                            v-model="selectedItem"
                            color="primary"
                        >
                            <v-list-item
                            class="my-2"
                            v-for="(item, i) in items"
                            :key="i"
                            @click="selectedItem = i"
                            >
                            <v-list-item-icon>
                                <v-icon v-text="item.icon"></v-icon>
                            </v-list-item-icon>
                            <v-list-item-content>
                                <v-list-item-title v-text="item.text"></v-list-item-title>
                            </v-list-item-content>
                            </v-list-item>
                        </v-list-item-group>
                    </v-list>
                </v-card>

                <v-card
                class="flex-grow-1 ma-auto pa-4"
                max-width="70%"
                >
                    <v-card-title v-text="resource.name"></v-card-title>
                    <v-card-subtitle v-text="resource.localisation"></v-card-subtitle>

                    <v-card-text>
                        {{ resource.description }}
                    </v-card-text>
                </v-card>
            </v-row>

            <v-card
            class="flex-grow-1 ma-auto pa-4"
            v-show="exists && updateTab == 0"
            >
                <v-card-title class="justify-center">Signaler une Anomalie</v-card-title>

                <v-divider></v-divider>

                <v-form
                ref="form"
                v-model="valid"
                lazy-validation
                >

                    <v-text-field
                    v-model="description"
                    :counter="150"
                    :rules="descriptionRules"
                    label="Description"
                    required
                    ></v-text-field>

                    <v-text-field
                    v-model="nom"
                    :counter="50"
                    :rules="nomRules"
                    label="Nom du Signaleur(optionel)"
                    required
                    ></v-text-field>

                    <v-btn
                    :disabled="!valid"
                    color="success"
                    class="mr-4"
                    @click="validate"
                    >
                    Validate
                    </v-btn>

                </v-form>

                <v-alert
                class="my-3"
                dismissible
                text
                type="success"
                v-model="added"
                >
                    Anomalie Signalée
                </v-alert>

            </v-card>

            <v-card
            class="flex-grow-1 ma-auto pa-4"
            v-show="exists && updateTab == 1"
            >
                <v-card-title class="justify-center">Les Tickets</v-card-title>

                <v-divider></v-divider>

                <v-list
                class="pa-0"
                two-line
                >
                    <v-virtual-scroll
                    :items="tickets"
                    :item-height="50"
                    height="400"
                    >
                        <template
                        v-slot:default="{ item }"
                        >
                            <v-list-item
                            :key="item._id"
                            >
                                <v-list-item-content>
                                    <v-list-item-title>Ticket #{{item._id}}</v-list-item-title>

                                    <v-list-item-subtitle v-text="item.name + ' - ' + item.date +' - ' + item.description"></v-list-item-subtitle>
                                </v-list-item-content>

                            </v-list-item>
                        </template>
                    </v-virtual-scroll>
                </v-list>
            </v-card>
        </v-col>
    </v-container>
</template>

<script>
export default {
    name: 'Resource',

    data: () => ({
        valid: true,
        show: false,
        added: false,
        resource: {name: '', _id: '', description: '', localisation: ''},
        exists: false,
        tickets: [],
        description: '',
        descriptionRules: [
            v => !!v || 'Description est requise',
            v => (v && v.length <= 150) || 'La Description doit etre 150 charactere max'
        ],
        nom: '',
        nomRules: [],
        selectedItem: 0,
        items: [
            { text: 'Signaler une Anomalie', icon: 'mdi-alert' },
            { text: 'Lister les Tickets d\'Anomalie de ce Resource', icon: 'mdi-format-list-bulleted'}
        ]
    }),
    methods: {
        validate: function() {
            this.$refs.form.validate();

            this.$http.put(`${this.$api}/tickets`, {'desc': this.description, 'res_id': this.resource._id, 'nom': this.nom}, {
                headers: {'Authorization': this.$cookies.get('Authorization')},
            })
            .then(() => {
                this.getTickets();
                this.added = true;
            });

            this.$refs.form.reset();
        },
        getResource: function() {
            this.$http.get(`${this.$api}/resources`, {
                headers: {'Authorization': this.$cookies.get('Authorization')},
                params: {'_id': this.$route.params._id}
            })
            .then(response => {
                this.resource._id = response.body._id;
                this.resource.description = response.body.description;
                this.resource.localisation = response.body.localisation;
                this.resource.name = `Resource #${this.resource._id}`;
                this.exists = true;
                this.getTickets();
            }, () => {
                this.exists = false;
                this.resource.name = `Erreur: Resource ${this.$route.params._id} n'existe pas`;
            })
        },
        getTickets: function() {
            this.$http.get(`${this.$api}/tickets`, {
                headers: {'Authorization': this.$cookies.get('Authorization')},
                params: {'res_id': this.$route.params._id}
            })
            .then(response => {
                this.tickets = response.body;
            });
        }
    },
    computed: {
        updateTab: function() {
            return this.selectedItem;
        }
    },
    created() {
        this.getResource();
    }
}
</script>