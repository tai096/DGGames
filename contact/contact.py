from flask import Blueprint, render_template

contact_blueprint = Blueprint('contact', __name__, template_folder='templates', static_folder='static', static_url_path='/assets')

@contact_blueprint.route('/contact', methods=["POST", "GET"])
def contact():
    return render_template('contact.html')