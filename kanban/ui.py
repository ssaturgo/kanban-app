from flask import session, request, jsonify, redirect, url_for
from flask.blueprints import Blueprint

bp = Blueprint('ui', __name__)


@bp.route('/set-theme', methods=['POST'])
def set_theme():
    data = request.get_json()

    # handle invalid requests
    if not data or 'theme' not in data:
        return jsonify(success=False, message='Invalid request'), 400

    # set theme
    if isinstance(data, dict):
        theme = data.get('theme')
        session['dark_mode'] = (theme == 'dark')
        print(f'theme set to {theme}')
        return jsonify(success=True, message='Successfully applied theme'), 200


@bp.route('/toggle-theme')
def toggle_theme():
    session['dark_mode'] = not session.get('dark_mode')
    return redirect(request.referrer)
