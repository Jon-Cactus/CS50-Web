document.addEventListener('DOMContentLoaded', function() {
    // Gain control of necessary DOM elements
    const form = document.getElementById('post-form');
    const postsDiv = document.querySelector('.posts-div');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        post();
    });

    // Handle post edits
    document.querySelectorAll('.edit-btn').forEach(element => {
        element.addEventListener('click', (event) => {
            const postDiv = event.target.closest('.post-div');
            let postText = postDiv.querySelector('.post-text').innerHTML; // Grab post text
            const postTextDiv = postDiv.querySelector('.post-text-div');
            const editBtn = postDiv.querySelector('.edit-btn');
            const editFormDiv = postDiv.querySelector('.edit-form-div');
            // toggle off original text display and edit button
            postTextDiv.style.display = 'none'; // Hide original text
            editBtn.style.display = 'none';

            if (!postDiv.querySelector('.edit-form')) {
                // take control of post-div here and display form
                editFormDiv.innerHTML =
                `<form class="edit-form">
                    <textarea id="edit-content" rows="5" cols="50" required>${postText}</textarea>
                    <div>
                        <button id="edit-post-save-btn" class="btn btn-primary">Save</button>
                        <a id="edit-post-cancel-btn" class="btn btn-outline-secondary">Cancel</a>
                    </div>
                </form>`

                const form = postDiv.querySelector('.edit-form');
                form.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const updatedContent = form.querySelector('#edit-content').value;
                    const postId = element.dataset.id;
                    const result = await editPost(postId, updatedContent);
                    if (result.success) { // Ensure result has been successfully retrieved
                        // Update UI with new post information without reloading
                        postDiv.querySelector('.post-text').innerHTML = result.content;
                        // Toggle on default post display and edit button
                        postTextDiv.style.display = 'block';
                        editBtn.style.display = 'block';
                        editFormDiv.innerHTML = ''; // Hide form
                    } else {
                        alert(`Error: ${result.error}`)
                    }
                });

                postDiv.querySelector('#edit-post-cancel-btn').addEventListener('click', () => {
                    editFormDiv.innerHTML = '';
                    postTextDiv.style.display = 'block';
                    editBtn.style.display = 'block';
                })
            }
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
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Fetch error:', error);
        alert('Failed to submit post. Check console for details.');
        return false;
    }
}

const editPost = async (postId, updatedContent) => {
    try {
        const response = await fetch(`/post/${postId}`, {
            method: 'PUT',
            body: JSON.stringify({
                updatedContent: updatedContent,
            })
        });
        const data = await response.json();
        if (response.ok && data.message) {
            return { success: true, content: data.post.content };
        } else {
            return { success: false, error: data.error };
        }
    } catch (error) {
        console.log('Error:', error);
        return { success: false, error: "Failed to update post" };
    }
}