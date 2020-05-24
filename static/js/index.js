/**
 * Copyright 2018, Google LLC
 * Licensed under the Apache License, Version 2.0 (the `License`);
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an `AS IS` BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';

window.addEventListener('load', function () {

    let uiConfig = {
        'signInSuccessUrl': '/stat',
        'signInOptions': [
            // Leave the lines as is for the providers you want to offer your users.
            firebase.auth.GoogleAuthProvider.PROVIDER_ID,
            firebase.auth.FacebookAuthProvider.PROVIDER_ID,
            firebase.auth.EmailAuthProvider.PROVIDER_ID
        ],
    };

    $('#sign-out').click(function () {
        // hide login information when user signs out
        firebase.auth().signOut().then(() => {
            // Clear the token cookie.
            document.cookie = "token=";
            window.location.href = '/';
        });
    });

    let ui;
    if (firebaseui.auth.AuthUI.getInstance()) {
        ui = firebaseui.auth.AuthUI.getInstance()
        ui.start('#firebaseui-auth-container', uiConfig)
    } else {
        ui = new firebaseui.auth.AuthUI(firebase.auth())
        ui.start('#firebaseui-auth-container', uiConfig)
    }

    firebase.auth().onAuthStateChanged(function (user) {
        if (user) {
            // User is signed in, so display the "sign out" button and login info.
            document.getElementById('firebaseui-auth-container').hidden = true;
            user.getIdToken().then(function (token) {
                // Add the token to the browser's cookies. The server will then be
                // able to verify the token against the API.
                // SECURITY NOTE: As cookies can easily be modified, only put the
                // token (which is verified server-side) in a cookie; do not add other
                // user information.
                document.cookie = "token=" + token;
            });
        } else {
            // User is signed out.
            // Initialize the FirebaseUI Widget using Firebase.
            // Show the Firebase login button.
            // Update the login state indicators.
            document.getElementById('firebaseui-auth-container').hidden = false;

            // Clear the token cookie.
            document.cookie = "token=";
        }
    }, function (error) {
        console.log(error);
        alert('Unable to log in: ' + error)
    });

});
