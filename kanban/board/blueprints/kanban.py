from flask import (Blueprint, flash, redirect, render_template,
                   request, session, url_for, jsonify, g)

from kanban.decorators import login_required

bp = Blueprint('kanban', __name__,
               static_folder='../static',
               template_folder='../templates'
               )


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


# load in user's information
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

