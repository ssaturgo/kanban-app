import json
import sqlite3

from flask import (Blueprint, flash, redirect, render_template,
                   request, session, url_for, jsonify, g, render_template_string)

from kanban.decorators import login_required

bp = Blueprint('kanban', __name__,
               static_folder='../static',
               template_folder='../templates'
               )


@login_required
@bp.route('/')
def index():
    db = g.db
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))  # or handle missing session

    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        return redirect(url_for('auth.login'))

    # Get or create board (using INSERT OR IGNORE for safety)
    board = db.execute(
        'SELECT * FROM boards WHERE owner_id = ?',
        (user_id,)
    ).fetchone()

    if board is None:
        db.execute(
            'INSERT INTO boards (owner_id, name) VALUES (?, ?)',
            (user_id, f"{user['display_name'] or user['name']}'s Board")
        )
        db.commit()  # 👈 commit after INSERT
        board = db.execute(
            'SELECT * FROM boards WHERE owner_id = ?',
            (user_id,)
        ).fetchone()

    board_id = board['id']
    session['board_id'] = board_id

    # Fetch columns
    columns = db.execute('SELECT * FROM columns WHERE board_id = ?', (board_id,)).fetchall()

    # Build sorted task lists (only if columns exist)
    sorted_tasks = {}
    for col in columns:
        col_id = col['id']
        tasks = db.execute('SELECT * FROM tasks WHERE column_id = ?', (col_id,)).fetchall()

        # Build ordered list using next_task_id chain
        sorted_tasks[col_id] = []
        current = next((t for t in tasks if t['previous_task_id'] is None), None)
        while current:
            sorted_tasks[col_id].append(current)
            current = next((t for t in tasks if t['id'] == current['next_task_id']), None)

    return render_template('pages/kanban.html', data={
        'columns': columns,
        'tasks': sorted_tasks,
        'board_id': board_id  # optional: pass to template
    })


@bp.route('/remove-column', methods=['POST'])
def remove_column():
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON Format'}), 400

    column_id = data.get('column_id')
    if not column_id:
        return jsonify({'error': 'Missing column_id'}), 400

    db: sqlite3.Connection = g.db

    db.execute('DELETE FROM tasks WHERE column_id = ?', (column_id,))
    print(f'deleted {db.total_changes} tasks')

    db.execute('DELETE FROM columns WHERE id = ?', (column_id,))
    if db.total_changes == 0:
        return jsonify({'error': 'Column not found'}), 404

    db.commit()
    print(f'column-{column_id} removed')

    return jsonify({'status': 'ok'})


@bp.route('/add-column', methods=['POST'])
def add_column():
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        return {'error': 'Invalid JSON Format'}, 400

    db: sqlite3.Connection = g.db

    # insert new column to database
    # (I just realized I never really used the position data of the columns D: )
    db.execute('INSERT INTO columns (board_id, position, name) VALUES (?,?,?)',
               (session['board_id'], data.get('position'), data.get('name')))
    db.commit()
    return redirect(request.referrer)


@bp.route('/remove-task', methods=['POST'])
def remove_task():
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        return {'error': 'Invalid JSON Format'}, 400
    task_id = data.get('task_id')

    db: sqlite3.Connection = g.db

    # check if task_id exists
    task = db.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone()
    if task:
        command = 'SELECT * FROM tasks WHERE id=?'
        previous_task = db.execute(command, (task['previous_task_id'],)).fetchone()
        previous_task_id = previous_task['id'] if previous_task else None
        next_task = db.execute(command, (task['next_task_id'],)).fetchone()
        next_task_id = next_task['id'] if next_task else None

        db.execute('UPDATE tasks SET next_task_id=? WHERE id=?', (next_task_id, previous_task_id))
        db.execute('UPDATE tasks SET previous_task_id=? WHERE id=?', (previous_task_id, next_task_id))

        db.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        db.commit()
        print('Successfully deleted task')
        return jsonify({'status': 'ok'}), 200
    else:
        print('Failed deleting task')
        return jsonify({'status': 'failed'}), 400


@bp.route('/move-task', methods=['POST'])
def move_task():
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        return {'error': 'Invalid JSON Format'}, 400
    task_id = data['task_id']
    target_column_id = data['new_column_id']

    db: sqlite3.Connection = g.db

    # update the current list
    task = db.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone()
    old_previous_task_id = task['previous_task_id']
    old_next_task_id = task['next_task_id']
    db.execute('UPDATE tasks SET next_task_id=? WHERE id=?', (old_next_task_id, old_previous_task_id))
    db.execute('UPDATE tasks SET previous_task_id=? WHERE id=?', (old_previous_task_id, old_next_task_id))

    # get the first task in the target column
    new_next_task = db.execute('SELECT * FROM tasks WHERE column_id=? AND previous_task_id is NULL',
                               (target_column_id,)).fetchone()
    new_next_task_id = new_next_task['id'] if new_next_task else None

    db.execute('UPDATE tasks SET column_id=?,previous_task_id=NULL, next_task_id=? WHERE id=?',
               (target_column_id, new_next_task_id, task_id))
    db.execute('UPDATE tasks SET previous_task_id=? WHERE id=?', (task_id, new_next_task_id))
    db.commit()
    print(f'Successfully moved task-{task_id} to column-{target_column_id}')

    return jsonify({
        'status': 'success',
        'message': 'Task updated',
    })


@bp.route('add-task', methods=['POST'])
def add_task():
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        return {'error': 'Invalid JSON Format'}, 400

    db: sqlite3.Connection = g.db

    # check if there already is a task in the column
    old_task = db.execute('SELECT * FROM tasks WHERE column_id=? AND previous_task_id is NULL',
                          (data.get('column_id'),)).fetchone()
    next_task_id = old_task['id'] if old_task else None

    # insert a new task
    new_task_id = db.execute('INSERT INTO tasks (column_id, previous_task_id, next_task_id, title, description) '
                             'VALUES (?,?,?,?,?)',
                             (data.get('column_id'),
                              None, next_task_id,
                              data.get('title'),
                              data.get('description')
                              )).lastrowid
    new_task = db.execute('SELECT * FROM tasks WHERE id=?', (new_task_id,)).fetchone()

    # if adding into existing task list, update the links to maintain the chain
    if old_task:
        # new_task -- next --> old_task
        db.execute('UPDATE tasks SET next_task_id=? WHERE id=?', (old_task['id'], new_task['id']))

        # new_task <-- previous -- old_task
        db.execute('UPDATE tasks SET previous_task_id=? WHERE id=?', (new_task['id'], old_task['id']))

    # commit all changes to the database
    db.commit()

    print("Task Added Successfully")

    template = '{% from "components/macros.html" import task_card %}{{ task_card(task) }}'
    task_html = render_template_string(template, task=new_task)
    return jsonify(html=task_html)


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

