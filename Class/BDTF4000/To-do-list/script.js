document.addEventListener('DOMContentLoaded', loadTasks);

const taskInput = document.getElementById('taskInput');
const addTaskBtn = document.getElementById('addTaskBtn');
const taskList = document.getElementById('taskList');
const filterButtons = document.querySelectorAll('.filter-btn');

// Event listener for adding a task
addTaskBtn.addEventListener('click', addTask);

// Add task function
function addTask() {
    const taskText = taskInput.value.trim();
    if (taskText) {
        const taskItem = document.createElement('li');
        taskItem.innerText = taskText;
        taskItem.addEventListener('click', toggleTask);
        
        const deleteBtn = document.createElement('button');
        deleteBtn.innerText = 'Delete';
        deleteBtn.addEventListener('click', deleteTask);
        taskItem.appendChild(deleteBtn);

        taskList.appendChild(taskItem);
        saveTasks();
        taskInput.value = '';  // Clear input field
    }
}

// Toggle task completion
function toggleTask(event) {
    const taskItem = event.target;
    taskItem.classList.toggle('completed');
    saveTasks();
}

// Delete task function
function deleteTask(event) {
    const taskItem = event.target.parentElement;
    taskItem.remove();
    saveTasks();
    event.stopPropagation();
}

// Filter tasks
filterButtons.forEach(btn => {
    btn.addEventListener('click', (event) => {
        const filter = event.target.dataset.filter;
        filterTasks(filter);
    });
});

function filterTasks(filter) {
    const tasks = document.querySelectorAll('li');
    tasks.forEach(task => {
        switch (filter) {
            case 'all':
                task.style.display = 'flex';
                break;
            case 'active':
                task.style.display = task.classList.contains('completed') ? 'none' : 'flex';
                break;
            case 'completed':
                task.style.display = task.classList.contains('completed') ? 'flex' : 'none';
                break;
        }
    });
}

// Save tasks to localStorage
function saveTasks() {
    const tasks = [];
    document.querySelectorAll('li').forEach(task => {
        tasks.push({
            text: task.firstChild.textContent,
            completed: task.classList.contains('completed')
        });
    });
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

// Load tasks from localStorage
function loadTasks() {
    const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    tasks.forEach(task => {
        const taskItem = document.createElement('li');
        taskItem.innerText = task.text;
        if (task.completed) taskItem.classList.add('completed');
        taskItem.addEventListener('click', toggleTask);
        
        const deleteBtn = document.createElement('button');
        deleteBtn.innerText = 'Delete';
        deleteBtn.addEventListener('click', deleteTask);
        taskItem.appendChild(deleteBtn);

        taskList.appendChild(taskItem);
    });
}
