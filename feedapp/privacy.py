from flask import Blueprint, render_template, request

bp = Blueprint('/privacy', __name__)


@bp.route('/privacy')
def privacy():
    id_token = request.cookies.get("token")

    sign_out_visibility = "hidden"
    name = ""

    if id_token:
        sign_out_visibility = ""

        from google.auth.transport import requests
        import google.oauth2.id_token
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, requests.Request())
            name = claims['email']
        except ValueError as e:
            pass

    return render_template('privacy.html', sign_out_visibility=sign_out_visibility, name=name)
