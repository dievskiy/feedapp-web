from flask import render_template, request, Blueprint, flash

bp = Blueprint('/', __name__)


@bp.route('/')
def root():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")

    name = ""
    sign_out_visibility = "hidden"
    if id_token:
        import google.oauth2.id_token
        from google.auth.transport import requests
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, requests.Request())
            name = claims['email']
            sign_out_visibility = ""
        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)
            if "expired" in error_message:
                error_message = "Please sign out and log in again."
            flash(error_message)

    return render_template('index.html', name=name, sign_out_visibility=sign_out_visibility)
