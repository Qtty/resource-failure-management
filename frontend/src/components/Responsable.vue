<template>
    <v-container class="d-flex flex-row align-start" v-if="is_resp">
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
                        v-for="(item, i) in items"
                        :key="i"
                        @click="updateData(i)"
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
            class="flex-grow-1 flex-shrink-0 mx-4 pa-4"
            v-show="updateTab == 0"
            >
                <v-card-title class="justify-center">Les Resources</v-card-title>

                <v-divider></v-divider>

                <v-list
                class="pa-0"
                two-line
                >
                    <v-virtual-scroll
                    :items="resources"
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
                                    <v-list-item-title>Resource #{{ item._id }}</v-list-item-title>

                                    <v-list-item-subtitle v-text="item.description + ' - ' + item.localisation"></v-list-item-subtitle>
                                </v-list-item-content>

                                <v-list-item-action class="d-flex flex-row">
                                    <v-btn
                                    class="mx-4"
                                    icon
                                    @click="visualise(item._id)"
                                    >
                                        <v-icon color="grey lighten-1">mdi-eye</v-icon>
                                    </v-btn>

                                    <v-btn
                                    icon
                                    @click="deleteResource(item._id)"
                                    >
                                        <v-icon color="grey lighten-1">mdi-minus</v-icon>
                                    </v-btn>
                                </v-list-item-action>
                            </v-list-item>
                        </template>
                    </v-virtual-scroll>
                </v-list>
            </v-card>

            <v-card
            class="flex-grow-1 flex-shrink-0 mx-4 pa-4"
            v-show="updateTab == 1"
            >
                <v-card-title class="justify-center">Ajouter une Ressource</v-card-title>

                <v-divider></v-divider>

                <v-form
                ref="form"
                v-model="valid"
                lazy-validation
                >

                    <v-text-field
                    v-model="description"
                    :counter="100"
                    :rules="descriptionRules"
                    label="Description"
                    required
                    ></v-text-field>

                    <v-text-field
                    v-model="localisation"
                    :counter="50"
                    :rules="localisationRules"
                    label="Localisation"
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
                    Resource Creé
                </v-alert>
            </v-card>

            <v-card
            class="flex-grow-1 flex-shrink-0 mx-4 pa-4"
            v-show="updateTab == 2"
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

                                <v-list-item-action>
                                    <v-btn
                                    icon
                                    @click="deleteTicket(item._id)"
                                    >
                                        <v-icon color="grey lighten-1">mdi-minus</v-icon>
                                    </v-btn>
                                </v-list-item-action>
                            </v-list-item>
                        </template>
                    </v-virtual-scroll>
                </v-list>
            </v-card>

    </v-container>
</template>

<script>
    export default {
        name: 'Responsable',

        data: () => ({
            valid: true,
            show: false,
            added: false,
            description: '',
            descriptionRules: [
                v => !!v || 'Description est requise',
                v => (v && v.length <= 100) || 'La Description doit etre 100 charactere max'
            ],
            localisation: '',
            localisationRules: [
                v => !!v || 'Localisation est requise',
                v => (v && v.length <= 50) || 'La Localisation doit etre 50 charactere max'
            ],
            is_resp: false,
            resources: [],
            tickets: [],
            selectedItem: 0,
            items: [
                { text: 'Lister les Ressources', icon: 'mdi-format-list-bulleted' },
                { text: 'Ajouter une Ressource', icon: 'mdi-projector' },
                { text: 'Lister les Tickets d\'Anomalie', icon: 'mdi-ticket-account'}
            ]
        }),
        methods: {
            getResources: function() {
                this.$http.get(`${this.$api}/responsable`, {
                    headers: {'Authorization': this.$cookies.get('Authorization')},
                    params: {'type': 'resource'}
                })
                .then(response => {
                    this.resources = response.body;
                    this.is_resp = true;
                }, () => {
                    this.is_resp = false;
                    this.$router.push('login');
                });
            },
            deleteResource: function(_id) {
                this.$http.delete(`${this.$api}/resources`, {
                    headers: {'Authorization': this.$cookies.get('Authorization')},
                    body: {'_id': _id}
                })
                .then(() => {
                    this.getResources();
                }, response => {
                    console.log(response);
                })
            },
            getTickets: function() {
                this.$http.get(`${this.$api}/tickets`, {
                    headers: {'Authorization': this.$cookies.get('Authorization')},
                    params: {'resp_id': true}
                })
                .then(response => {
                    this.tickets = response.body;
                });
            },
            deleteTicket: function(_id) {
                this.$http.delete(`${this.$api}/tickets`, {
                    headers: {'Authorization': this.$cookies.get('Authorization')},
                    body: {'_id': _id}
                })
                .then(() => {
                    this.getTickets();
                })
            },
            visualise: function(_id) {
                this.$router.push(`/etiquette/${_id}`);
            },
            validate: function() {
                this.$refs.form.validate();

                this.$http.put(`${this.$api}/resources`, {'desc': this.description, 'loc': this.localisation}, {
                    headers: {'Authorization': this.$cookies.get('Authorization')},
                })
                .then(response => {
                    console.log(response);
                    this.added = true;
                });

                this.$refs.form.reset();
            },
            updateData: function(i) {
                this.selectedItem = i;

                if (i == 0)
                    this.getResources();

                if (i == 2)
                    this.getTickets();
            }
        },
        computed: {
            updateTab: function() {
                return this.selectedItem;
            }
        },
        created() {
            this.getResources();
        }
    }
</script>
