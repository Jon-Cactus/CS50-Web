document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('post-form');
    form.addEventListener('submit', function(event) {
        console.log('Submit event listener triggered');
        event.preventDefault();
        post();
    });
});

async function post() {
    try {
        const content = document.getElementById('content').value;
        if (!content) {
            alert('Post content cannot be empty!');
            return;
        }
        const response = await fetch('/post', {
            method: 'POST',
            body: JSON.stringify({
                content: content
            })
        });
        const data = await response.json();
        if (response.ok) {
            document.querySelector('#content').value = '';
            console.log("Text area cleared");
            alert('Post shared successfully!');
        } else {
            alert(`Error: ${data.error || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Fetch error:', error);
        alert('Failed to submit post. Check console for details.');
        return false;
    }
}