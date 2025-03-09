

document.addEventListener('DOMContentLoaded', () => {
    const submit = document.getElementById('submit');
    const newTask = document.getElementById('task');
    let tasks = JSON.parse(localStorage.getItem('tasks'));
    
    if (tasks === null) {
        tasks = [];
        const li = document.createElement('li');
        li.innerHTML = "No tasks yet!";
        document.getElementById('tasks').append(li);
    } else {
        for (let task of tasks) {
            const li = document.createElement('li');
            li.innerHTML = task;
            document.getElementById('tasks').append(li);
        }
    }
    
    submit.disabled = true;
    newTask.onkeyup = () => {
        if (newTask.value.length > 0) {
            submit.disabled = false;
        }
        else {
            submit.disabled = true;
        }
    }

    document.querySelector('form').onsubmit = () => {
        if (tasks.length === 0) {
            document.querySelector('li').remove()
        }
        const task = newTask.value;
        tasks.push(task)  
        localStorage.setItem('tasks', JSON.stringify(tasks))
        newTask.value = '';
        const li = document.createElement('li');
        li.innerHTML = task;
        document.getElementById('tasks').append(li);

        submit.disabled = true;

        return false;
    }
})