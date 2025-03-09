window.onpopstate = (e) => {
    console.log(e.state.section);
    showSection(e.state.section);
}

function showSection(section) {
    fetch(`sections/${section}`)
    .then(response => response.text())
    .then(text => {
        console.log(text);
        document.querySelector('#content').innerHTML = text;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            const section = this.dataset.section;

            history.pushState({section: section}, "", `section/${section}`);
            showSection(section);
        }
    })
})