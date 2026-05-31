const board = document.getElementById('kb-board');

// ========================
// Helpers
// ========================

const getClosest = (target, selector) => target.closest(selector);

const postJSON = async (url, body) => {
    // perform a POST request and await response
    const result = await fetch(url, {
        method:"POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    });

    if (!result.ok) {
        throw new Error(`${result.status}: ${result.statusText}`);
    }

    return await result.json();
}

// ========================
// Events Handling
// ========================

board.addEventListener('click', async (e) => {
    const addBtn = getClosest(e.target, '.btn-add-task');
    if (addBtn) {
        const columnID = addBtn.dataset.columnId;
        console.log(`Adding new task to column-${columnID}`);

        try {
            const {html} = await postNewTask(columnID);
            const column = board.querySelector(`#column-${columnID}`);
            column?.insertAdjacentHTML('afterbegin', html);
        } catch (error) {
            console.error("Failed to add new task: ", error);
            alert("Failed to add new task");
        }
        return;
    }

    const removeBtn = getClosest(e.target, '.btn-remove-task');
    if (removeBtn) {
        const taskID = removeBtn.dataset.taskId;
        console.log(`Removing task-${taskID}`);

        try {
            await postRemoveTask(taskID);
            const task = board.querySelector(`#task-${taskID}`);
            task?.remove()
        } catch (error) {
            console.error(`Failed to remove task-${taskID}`, error);
            alert("Failed to remove task");
        }
    }

    const removeColumnBtn = getClosest(e.target, '.btn-remove-column');
    if (removeColumnBtn) {
        const columnId = removeColumnBtn.dataset.columnId;
        const columnName = removeColumnBtn.dataset.columnName;
        await removeColumn(columnId, columnName);
    }
});

// ========================
// 🎯 DRAG & DROP
// ========================
    // dragging
document.addEventListener('dragstart', (e) => {
    const task = getClosest(e.target, '.kb-task-wrapper');
    if (!task) return;

    e.dataTransfer.setData('text/plain',task.dataset.taskId);
    e.dataTransfer.effectAllowed = 'move';
    task.classList.add('dragging');
});

    // dragging over
document.addEventListener('dragover', (e) => {
    e.preventDefault();
    const column = getClosest(e.target, '.kb-task-list');
    if (column) {
        e.dataTransfer.dropEffect = 'move';
    }
});

    // dropping
document.addEventListener('drop', async (e) => {
    e.preventDefault();

    const taskID = e.dataTransfer.getData('text/plain');
    const column = getClosest(e.target, '.kb-task-list');
    const task = document.getElementById(`task-${taskID}`);

    if (!column || !task) return;

    // drop logic
    const currentColumn = task.closest('.kb-task-list');
    const newColumnID = parseInt(column.dataset.columnId);
    const oldColumnID = currentColumn ? parseInt(currentColumn.id.replace('column-', '')):null;

    // skip if dropping to the same column
    if (newColumnID === oldColumnID) {
        console.log("Not moved, dropped to the same column")
    }

    // move to new column
    try {
        await postMoveTask(taskID, newColumnID);
        column.prepend(task);
        console.log(`task-${taskID} moved to column-${newColumnID}`);
    } catch (error) {
        console.log(`failed to move task-${taskID}`);
        alert('Move failed')
    }
})

document.addEventListener('dragend', (e) => {
  const task = getClosest(e.target, '.kb-task-wrapper');
  task?.classList.remove('dragging');
})

// ========================
// API Stuff
// ========================
async function postNewTask(columnID) {
    let title = prompt('Task title:');
    if (!title) title = "New Task"
    let description = prompt('Task description:');
    if (!description) description = "...";

    return postJSON('/kanban/add-task', {
        column_id: columnID,
        title: title,
        description: description
    });
}

async function postRemoveTask(taskID) {
    return postJSON('/kanban/remove-task', {
        task_id: taskID
    })
}

async function postMoveTask(taskID, targetColumnID) {
    return postJSON('/kanban/move-task', {
        task_id: taskID,
        new_column_id: targetColumnID
    });
}

// after this point; I think I am in too much of a mess
// I will do rough not optimized prototypes to finish the project
// so I can restructure and redo this project from the ground up

async function addColumn() {
    const name = prompt('Enter column name:');
    if (!name) return;

    try {
        const res = await fetch('/kanban/add-column', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                name: name,
                board_id: 1,
                position: 1,
            })
        });
        if (!res.ok) throw new Error('Failed');
        location.reload();
    } catch (err) {
        alert('Failed to add column');
    }
}

async function removeColumn(columnId, columnName) {
  if (!confirm(`Delete column "${columnName}"? This cannot be undone.`)) return;

  try {
    const result = await fetch('/kanban/remove-column', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ column_id: columnId })
    });

    if (!result.ok) {
      const errorData = await result.json().catch(() => ({ error: '' }));
      throw new Error(errorData.error || `HTTP ${result.status}`);
    }

    const column = document.getElementById(`column-${columnId}`)?.closest('.kb-column');
    column?.remove();
    console.log(`column-${columnId} removed`);
  } catch (err) {
    console.error('Failed to remove column:', err);
    alert('Failed to remove column');
  }
}