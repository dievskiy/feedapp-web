import google.oauth2.id_token
from flask import render_template, request, Blueprint, flash
from google.auth.transport import requests

firebase_request_adapter = requests.Request()

bp = Blueprint('/', __name__)


@bp.route('/')
def root():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")

    name = ""
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            name = claims['email']
            pass

        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)
            if "expired" in error_message:
                error_message = "Please sign out and log in again."
            flash(error_message)

    return render_template('index.html', name=name)
