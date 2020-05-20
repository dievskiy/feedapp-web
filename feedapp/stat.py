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
initialize_app()

db = firestore.client()

months_reference = None


# return nutrient data for specific month
@bp.route('/stat/data', methods=["GET"])
def get_month_statistics():
    month_str = request.args.get('month')
    return get_nutrient_for_month(month_str)


def get_nutrient_for_month(month_num, dictionary=False):
    """
    returns json of days with nutrients for specific day
    :param dictionary:
    :param month_num: in 1-based format (1 - January)
    :return: JSON or dictionary
    """
    try:
        if months_reference is None or month_num is None:
            return ""

        # receive CollectionReference for requested month
        months = [m for m in months_reference.collections() if m.id == month_num]

        # get DocumentReference for each day
        days_ref = months[0].list_documents()

        days = []
        for day_ref in days_ref:
            days.append(day_ref.get().to_dict())

        if dictionary:
            return calculator.count_nutrients(days)
        else:
            return jsonify({'days': calculator.count_nutrients(days)})
    except ValueError as error:
        return ""


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
        return render_template('index.html')


@bp.route('/stat/savepdf/<string:month_num_str>', methods=['GET'])
def save_pdf(month_num_str):
    try:
        # get days with nutrition data
        days = get_nutrient_for_month(month_num_str, dictionary=True)
        if not days:
            raise ValueError()

        plotter = nc.NutrientsPlotter(days)
        calories_image_bytes, other_image_bytes = plotter.get_encoded_images_bytes()

        # insert images into html
        calories_image = '<img src="data:image/png;base64, {}">'.format(calories_image_bytes.decode('utf-8'))
        other_nutrients_image = '<img src="data:image/png;base64, {}">'.format(other_image_bytes.decode('utf-8'))

        from feedapp import utils
        html = render_template('statistics_pdf.html', calories=calories_image,
                               other_nutrients_image=other_nutrients_image,
                               month_name=utils.get_name_for_month(month_num_str))

        from feedapp import pdfgenerator
        # get pdf from html
        response = pdfgenerator.render_pdf(html)
        headers = {
            'content-type': 'application.pdf',
            'content-disposition': 'inline; filename=statistics.pdf'}
        response.headers = headers
        return response
    except ValueError as err:
        flash("Invalid month. Probably there is no tracked days in that month. ")
        return render_template('base.html')


@bp.route('/<int:id>', methods=['GET'])
def month(id):
    return str(id)
