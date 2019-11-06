/*
 * agnoMirror.js
 *
 * This script is the main script in the agnoMirror MagicMirror Module.
 * It is responsible for handling login/logout actions and for displaying notifications 
 * 
 *
 * @author: Lucas Mahler @Lugges991
 *
 */
'use strict';


Module.register("agnoMirror", {
    defaults: {
        // Module set used for strangers and if no user is detected
        // defaultClass: "default",
        defaultClass: "unknown",
        // Set of modules which should be shown for every user
        // everyoneClass: "everyone",
        everyoneClass: "known",
        // Boolean to toggle welcomeMessage
        welcomeMessage: true,
        // recognition interval 
        interval: 2,
        // delay in seconds after which the user gets logged out if he is not recognized
        logoutDelay: 20

    },
    timeouts: {},
    users: [],

    start: function() {
        Log.log("Starting module: " + this.name);
        this.sendSocketNotification('CONFIG', this.config);
        Log.log("Starting module: " + this.name);
    },
    login_user: function(name) {
        var self = this;

        MM.getModules()
            .withClass(this.config.defaultClass)
            .exceptWithClass(this.config.everyoneClass)
            .enumerate(function(module) {
                module.hide(self.config.animationSpeed, function() {
                    Log.log(module.name + ' is hidden.');
                }, {
                    lockString: self.identifier
                });
            });

        MM.getModules()
            .withClass(name.toLowerCase())
            .enumerate(function(module) {
                module.show(self.config.animationSpeed, function() {
                    Log.log(module.name + ' is shown.');
                }, {
                    lockString: self.identifier
                });
            });

        if (this.config.welcomeMessage) {
            var person = name;
            // We get Unknown from Face-Reco and then it should be translated to stranger
            if (person === 'Unknown') {
                person = 'stranger';
            }

            this.sendNotification("SHOW_ALERT", {
                type: "notification",
                message: "Hello, " + person,
                title: "Welcome to the agnoMirror!"
            });
        }
    },

    logout_user: function(name) {
        var self = this;

        MM.getModules()
            .withClass(name.toLowerCase())
            .enumerate(function(module) {
                module.hide(self.config.animationSpeed, function() {
                    Log.log(module.name + ' is hidden.');

                }, {
                    lockString: self.identifier
                });
            });

        if (this.users.length === 0) {
            MM.getModules()
                .withClass(self.config.defaultClass)
                .exceptWithClass(self.config.everyoneClass)
                .enumerate(function(module) {
                    module.show(self.config.animationSpeed, function() {
                        Log.log(module.name + ' is shown.');
                    }, {
                        lockString: self.identifier
                    });
                });
        }
    },

    socketNotificationReceived: function(notification, payload) {
        var self = this;
        
        // somebody has logged in
        if (payload.action == "login") {
            for (var user of payload.users) {
                if (user != null) {
                    this.users.push(user);
                    this.login_user(user);

                    if (this.timouts[user] != null) {
                        clearTimeout(this.timouts[user]);
                    }
                }
            }

            this.sendNotification("USERS_LOGIN", payload.users);
        }

        // somebody has logged out
        else if (payload.action == "logout") {
            for (var user of payload.users) {
                if (user != null) {
                    this.timouts[user] = setTimeout(function() {
                        self.users = self.users.filter(function(u) {
                            return u !== user
                        });
                        self.logout_user(user);
                    }, this.config.logoutDelay);
                }
            }

            this.sendNotification("USERS_LOGOUT", payload.users);
        }
    },

    notificationReceived: function(notification, payload, sender) {

        var self = this;

        // Event if DOM is created
        if (notification === 'DOM_OBJECTS_CREATED') {
            // Show all Modules with default class
            MM.getModules()
                .exceptWithClass(this.config.defaultClass)
                .enumerate(function(module) {
                    module.hide(0, function() {
                        Log.log('Module is hidden.');
                    }, {
                        lockString: self.identifier
                    });
                });
        }

        // load logged in users
        if (notification === 'GET_LOGGED_IN_USERS') {
            Log.log(this.name + ' get logged in users ' + this.users);
            this.sendNotification("LOGGED_IN_USERS", this.users);
        }
    }


});
