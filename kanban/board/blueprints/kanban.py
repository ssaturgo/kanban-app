from flask import (Blueprint, flash, redirect, render_template,
                   request, session, url_for, jsonify, g)

from kanban.utilities import login_required

bp = Blueprint('kanban', __name__,
               static_folder='../static',
               template_folder='../templates'
               )


# login page
@login_required
@bp.route('/')
def index():
    return render_template('pages/kanban.html')


@bp.route('/update-task', methods=['POST'])
def update_task():
    data = request.json

    print(f'Server received: {data}')
    return jsonify({
        'status': 'success',
        'message': 'Task updated',
    })


@bp.route('/toggle-theme')
def toggle_theme():
    session['dark_mode'] = not session.get('dark_mode', False)
    return redirect(request.referrer)


@bp.context_processor
def inject_theme():
    return dict(dark_mode=session.get('dark_mode', False))

@bp.context_processor
def inject_user():
    command = 'SELECT display_name FROM users WHERE id=?'
    user_id = session['user_id']
    display_name = 'Guest'

    if user_id:
        user = g.db.execute(command, (user_id,)).fetchone()
        if user:
            display_name = user['display_name']

    g.display_name = display_name
    return dict(display_name=display_name)

