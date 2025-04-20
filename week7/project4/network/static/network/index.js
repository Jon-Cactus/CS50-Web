document.addEventListener('DOMContentLoaded', function() {
    // Gain control of necessary DOM elements
    const postForm = document.getElementById('post-form');
    const postsDiv = document.querySelector('.posts-div');
    const toggleFollowBtn = document.getElementById('toggle-follow-btn');

    // Handle post form submission
    if (postForm) {
        postForm.addEventListener('submit', function(e) {
            e.preventDefault();
            post();
        });
    }

    // Handle follow toggling
    if (toggleFollowBtn) {
        toggleFollowBtn.addEventListener('click', async (event) => {
            const username = event.target.dataset.username;
            if (!username) {
                alert('Username missing');
                return;
            }
            const result = await toggleFollow(username);
            if (result.success) {
                if (result.following) {
                    alert("Successfully followed user")
                } else {
                    alert("Successfully unfollowed user")
                }
                console.log(result.follower_count);
                // Update follower count on profile page
                const followerCount = document.getElementById('follower-count');
                followerCount.innerText = `Followers: ${result.follower_count}`;
                toggleFollowBtn.innerText = result.following ? 'Unfollow' : "Follow";
            } else {
                alert(`Error: ${result.error}`);
            }
        });
    }
    

    // Handle post edits
    if (postsDiv) {
        postsDiv.querySelectorAll('.edit-btn').forEach(element => {
            element.addEventListener('click', (event) => { // Add event listeners to each btn
                const postDiv = event.target.closest('.post-div');
                let postText = postDiv.querySelector('.post-text').innerHTML; // Grab post text
                const postTextDiv = postDiv.querySelector('.post-text-div');
                const editBtn = postDiv.querySelector('.edit-btn');
                const editFormDiv = postDiv.querySelector('.edit-form-div');
                // Toggle off original text display and edit button
                postTextDiv.style.display = 'none'; // Hide original text
                editBtn.style.display = 'none';
        
                if (!postDiv.querySelector('.edit-form')) {
                    // Take control of post-div here and display form
                    editFormDiv.innerHTML =
                    `<form class="edit-form">
                        <textarea id="edit-content" rows="5" cols="50" required>${postText}</textarea>
                        <div>
                            <button id="edit-post-save-btn" class="btn btn-primary">Save</button>
                            <a id="edit-post-cancel-btn" class="btn btn-outline-secondary">Cancel</a>
                        </div>
                    </form>`
        
                    const editForm = postDiv.querySelector('.edit-form');
                    editForm.addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const updatedContent = editForm.querySelector('#edit-content').value;
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
    }
    
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

const toggleFollow = async (username) => {
    try {
        const response = await fetch(`/profile/${username}/follow-toggle`,{
            method: 'POST',
        });
        const data = await response.json();
        if (response.ok) {
            return {
                success: true,
                following: data.following,
                message: data.message,
                follower_count: data.follower_count
            };
        } else {
            return { success: false, error: data.error }
        }
    } catch (error) {
        console.error('Error:', error);
        return { success: false, error: error.message }
    }
}