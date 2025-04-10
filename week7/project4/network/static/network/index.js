document.addEventListener('DOMContentLoaded', function() {

    // Grab form and change its onsubmit to call post function
    const form = document.getElementById('post-form');
    if (!form) {
        console.log("Form not found");
        alert('Form not found: check HTML');
        return;
    }
    console.log('Attaching onsubmit handler');
    form.onsubmit = function(event) {
        console.log("Form submission triggered");
        event.preventDefault();
        console.log("Default submission prevented");
        post();
        return false;
    };

    form.addEventListener('submit', function(event) {
        console.log('Submit event listener triggered');
        event.preventDefault();
        post();
    })
})

async function post() {
    try {
        console.log("Starting to fetch post");
        const content = document.getElementById('content').value;
        console.log('Content:', content)
        const response = await fetch('/post', {
            method: 'POST',
            body: JSON.stringify({
                content: content
            })
        })
        const data = await response.json();
        console.log('Response data:', data);
        if (response.ok) {
            document.querySelector('#content').value = '';
            console.log("Text area cleared");
        }
    } catch (error) {
        console.log('Fetch error:', error);
    }
}

window.debugLog = window.debugLog || [];
window.debugLog.push('Script loaded at ' + new Date().toISOString());