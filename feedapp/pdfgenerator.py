from xhtml2pdf import pisa
from io import StringIO, BytesIO
from flask import make_response


def render_pdf(html):
    """
    function to generate pdf from html
    :param html: html to
    :return:
    """
    pdf = BytesIO()
    pisa.CreatePDF(StringIO(html), pdf)
    response = make_response(pdf.getvalue())
    pdf.close()
    return response
