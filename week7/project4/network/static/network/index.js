document.addEventListener('DOMContentLoaded', function() {
    // Gain control of necessary DOM elements
    const form = document.getElementById('post-form');
    const postsDiv = document.querySelector('.posts-div');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        post();
    });

    // Add event listeners
    querySelectorAll('.edit-text').forEach(element => {
        element.addEventListener('click', (event) => {
            // take control of post-div here and display form
        });
    });
});

const post = async () => {
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
            console.log('Post shared successfully!');
        } else {
            alert(`Error: ${data.error || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Fetch error:', error);
        alert('Failed to submit post. Check console for details.');
        return false;
    }
}
// Current format will not work -- will trigger function when clicking anywhere on the post.
// Find a way to isolate the eventListener to the edit-txt alone
const editPost = async (event) => {
    try {
        const postId = event.target.dataset.id;
        if (!postId) {
            console.log("Error: Problem accessing post");
            return;
        }
        const response = await fetch(`/post/${postId}`)
    }
}