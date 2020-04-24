import google.oauth2.id_token
from firebase_admin import credentials, firestore, initialize_app
from flask import (
    Blueprint, jsonify, flash)
from flask import render_template, request
from google.auth.transport import requests
from . import nutcalculator as nc

bp = Blueprint('stat', __name__)

calculator = nc.NutrientCalculator()

firebase_request_adapter = requests.Request()

# Initialize Firestore DB
# cred = credentials.Certificate('kkk.json')
initialize_app()

db = firestore.client()

months_reference = None


# return nutrient data for specific month
@bp.route('/stat/data', methods=["GET"])
def get_month_statistics():
    month = request.args.get('month')
    return get_nutrient_for_month(month)


def get_nutrient_for_month(month):
    if months_reference is None or month is None:
        return "{}"

    # receive CollectionReference for requested month
    months = [m for m in months_reference.collections() if m.id == month]

    # get DocumentReference for each day
    days_ref = months[0].list_documents()

    days = []
    for day_ref in days_ref:
        days.append(day_ref.get().to_dict())

    return jsonify({'days': calculator.count_nutrient(days)})


@bp.route('/stat', methods=['GET', 'POST'])
def root():
    try:
    # Check if ID was passed to URL query
        id_token = request.cookies.get("token")
        if id_token:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            user_id = claims['user_id']
            if user_id:
                global months_reference
                # get document that contains list of months
                months_reference = db.document(u'users/{0}/days/2020'.format(str(user_id)))
                # receive that sequence of CollectionReference and get it's id
                months = [m.id for m in months_reference.collections()]
        return render_template('statistics.html', months=months, name=claims['email'])
    except:
        flash("Sign in to view statistics.")
        return render_template('base.html')


@bp.route('/<int:id>', methods=['GET'])
def month(id):
    return str(id)
