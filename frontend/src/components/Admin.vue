<template>
    <v-container class="d-flex flex-row align-start" v-if="is_admin">
            <v-card
            class="pa-1"
            max-width="280"
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
                        @click="updateAdding(i)"
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
            v-show="!is_adding"
            >
                <v-card-title class="justify-center">Responsables de Maintenance</v-card-title>

                <v-divider></v-divider>

                <v-list
                class="pa-0"
                two-line
                >
                    <v-virtual-scroll
                    :items="resps"
                    :item-height="50"
                    height="400"
                    >
                        <template
                        v-slot:default="{ item }"
                        >
                            <v-list-item
                            :key="item.nom"
                            >
                                <v-list-item-content>
                                    <v-list-item-title v-text="item.nom + ' ' + item.prenom"></v-list-item-title>

                                    <v-list-item-subtitle v-text="item.mail"></v-list-item-subtitle>
                                </v-list-item-content>

                                <v-list-item-action>
                                    <v-btn
                                    icon
                                    @click="deleteResp(item._id)"
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
            v-show="is_adding"
            >
                <v-card-title class="justify-center">Ajouter un Responsable de Maintenance</v-card-title>

                <v-divider></v-divider>

                <v-form
                ref="form"
                v-model="valid"
                lazy-validation
                >

                    <v-text-field
                    v-model="nom"
                    :rules="nomRules"
                    label="Nom"
                    required
                    ></v-text-field>

                    <v-text-field
                    v-model="prenom"
                    :rules="prenomRules"
                    label="Prenom"
                    required
                    ></v-text-field>

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

                </v-form>
            </v-card>

    </v-container>
</template>

<script>
    export default {
        name: 'Admin',

        data: () => ({
            valid: true,
            show: false,
            email: '',
            emailRules: [
                v => !!v || 'E-mail is required',
                v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
            password: '',
            passwordRules: [v => !!v || 'Password is required',],
            nom: '',
            nomRules: [v => !!v || 'Nom is required'],
            prenom: '',
            prenomRules: [v => !!v || 'Prenom is required'],
            is_adding: false,
            is_admin: false,
            resps: [],
            selectedItem: 0,
            items: [
                { text: 'Lister les Responsables', icon: 'mdi-format-list-bulleted' },
                { text: 'Ajouter un Responsable', icon: 'mdi-account' },
            ]
        }),
        methods: {
            getResps: function() {
                this.$http.get(`${this.$api}/admin`, {
                    headers: {'Authorization': this.$cookies.get('Authorization')}
                })
                .then(response => {
                    console.log(response);
                    this.resps = response.body;
                    this.is_admin = true;
                }, response => {
                    this.is_admin = false;
                    console.log(response);
                });
            },
            deleteResp: function(_id) {
                console.log(_id);
                this.$http.delete(`${this.$api}/admin`, {
                    headers: {'Authorization': this.$cookies.get('Authorization')},
                    body: {'_id': _id}
                })
                .then(response => {
                    console.log(response);
                    this.getResps();
                }, response => {
                    console.log(response);
                })
            },
            updateAdding: function(action) {
                this.is_adding = action;
            },
            validate: function() {
                this.$refs.form.validate();

                this.$http.put(`${this.$api}/admin`, {'nom': this.nom, 'prenom': this.prenom, 'mail': this.email, 'password': this.password}, {
                    headers: {'Authorization': this.$cookies.get('Authorization')},
                })
                .then(response => {
                    console.log(response);
                    this.getResps();
                })
            }
        },
        created() {
            this.getResps();
        }
    }
</script>
