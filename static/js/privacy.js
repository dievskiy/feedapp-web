window.onload = function () {
    $('#sign-out').click(function () {
        // hide login information when user signs out
        firebase.auth().signOut().then(() => {
            // Clear the token cookie.
            document.cookie = "token=";
            window.location.href = '/';

        });
    });

}