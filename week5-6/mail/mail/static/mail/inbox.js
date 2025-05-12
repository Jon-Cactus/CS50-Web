document.addEventListener('DOMContentLoaded', function() {
  // Store views
  const emailView = document.getElementById('email-view');
  const composeView = document.getElementById('compose-view');
  const emailsView = document.getElementById('emails-view');

  // Noticed repeated code for toggling different views (ternary operator learned from FreeCodeCamp)
  // determine the correct view to display
  const toggleViews = (mailbox) => {
    emailsView.style.display = mailbox === 'emails' ? 'block' : 'none';
    emailView.style.display = mailbox === 'email' ? 'block' : 'none';
    composeView.style.display = mailbox === 'compose' ? 'block' : 'none';
  }

  const loadMailbox = (mailbox) => {
    // Show the mailbox and hide other views
    toggleViews('emails');
    // Show the mailbox name
    emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    emailsView.dataset.mailbox = mailbox; // This was the only way I could properly add the correct eventlistener
    // Load all mail in a given mailbox
    loadMail(mailbox, emailsView);
  }

  function composeEmail(sender, subject, body, timestamp) {
    // Show compose view and hide other views
    toggleViews('compose');
    // Store compose inputs
    const composeRecipients = document.querySelector('#compose-recipients');
    const composeSubject = document.querySelector('#compose-subject');
    const composeBody = document.querySelector('#compose-body');
    // When 'reply' button is clicked
    if (arguments.length >= 4) {
      try {
        composeRecipients.value = sender;
        composeRecipients.setAttribute('disabled', true);
        composeSubject.value =`Re: ${subject}`;
        composeBody.value = `\n\n\nOn ${timestamp}, ${sender} wrote:\n ${body}`
      } catch (error) {
        console.error('Error setting compose fields:', error);
      }      
    } else {
      // Clear out composition fields
      composeRecipients.value = '';
      composeRecipients.removeAttribute('disabled');
      composeSubject.value = '';
      composeBody.value = '';
    }
  }

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => loadMailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => loadMailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => loadMailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => composeEmail());
  document.querySelector('#compose-form').onsubmit = () => sendMail(emailsView); // Send Mail

  // Add event listener for email clicks once
  emailsView.addEventListener('click', (event) => handleEmailPreviewClick(event, emailsView, emailView, toggleViews))
    
  const handleEmailPreviewClick = async (event, emailsView, emailView, toggleViews) => {
    const emailPreview = event.target.closest('.email-preview');
    if (!emailPreview) return;
    const emailId = emailPreview.dataset.id;
    const mailbox = emailsView.dataset.mailbox; // Get current mailbox type

    try {
      const email = await fetchEmail(emailId)
          // Render email
          toggleViews('email');
          emailView.innerHTML = '';
          const emailDiv = document.createElement('div');
          emailDiv.innerHTML = `
            <p><strong>From: </strong>${email.sender}</p>
            <p><strong>To: </strong>${email.recipients}</p>
            <p><strong>Subject: </strong>${email.subject}</p>
            <p><strong>Timestamp: </strong>${email.timestamp}</p>
            <hr></hr>
            <p>${email.body}</p>
          `;
          if (mailbox === 'inbox') {
            emailDiv.innerHTML += `
              <div>
                <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
                <button class="btn btn-sm btn-outline-primary" id="unread">Mark as unread</button>
                <button class="btn btn-sm btn-outline-primary" id="archive">Archive</button>
              </div>
            `;
            await updateMailStatus(emailId, "read", true); // Mark as read only for inbox
          } else if (mailbox === 'archive') {
            emailDiv.innerHTML += '<button class="btn btn-sm btn-outline-primary" id="unarchive">Unarchive</button>';
          }

          emailView.append(emailDiv);
          // Add event listeners to buttons
          if (mailbox === 'inbox') {
            document.getElementById('reply').addEventListener('click', () => {
              console.log('Reply clicked for email:', email);
              composeEmail(email.sender, email.subject, email.body, email.timestamp); // Pre-fill composeView
            })
            document.getElementById('unread').addEventListener('click', async () => {
              await updateMailStatus(emailId, "read", false);
            });
            document.getElementById('archive').addEventListener('click', async () => {
              await updateMailStatus(emailId, "archived", true);
              loadMailbox('inbox');
                /* I learned my lesson after trying to get away with calling a function that includes
                 a fetch call and then calling a function directly after it without
                 chaining it with `.then(...)` or using `await`. The second function may be called before the 
                 fetch call completes, creating a race condition (thanks ddb). */
            });
          } else if (mailbox === 'archive') {
            document.getElementById('unarchive').addEventListener('click', async () => {
              await updateMailStatus(emailId, "archived", false);
              loadMailbox('inbox');
            });
          } 
    } catch (error) {
      console.log('Error', error);
    }
  };
  loadMailbox('inbox');
});

// Loads mail in the appropriate mailbox
async function loadMail(mailbox, emailsView) {
  try {
    emailsView.innerHTML = '';
    const response = await fetch(`/emails/${mailbox}`);
    const emails = await response.json();
    let html = '';
    emails.forEach(email => {
      // Add 'read' class if the email in the inbox and has been opened
      const readClass = mailbox === 'inbox' && email.read ? 'read' : '';
      html += `
      <div class="email-preview ${readClass}" data-id="${email.id}">
        <span><strong>${email.sender}</strong></span>
        <span>${email.subject}</span>
        <span>${email.timestamp}</span>
      </div>
      `;
    });
    emailsView.innerHTML = html;
  } catch (error) {
    console.log('Error', error);
  }
}

async function fetchEmail(emailId) {
  try {
    const response = await fetch(`/emails/${emailId}`);
    const data = await response.json();
    console.log(data);
    console.log(data);
    return data;
  } catch (error) {
    console.log("Error:", error);
  }
}
// After many issues and searching, it turned out that the only way I could find to solve my
// issue of not seeing 'read' or 'archived' status changes immediately following clicking an email,
// 'unread' button, 'archive' button, or 'unarchive' button, 
// was by implementing an asynchronous function here
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function
async function updateMailStatus(id, category, value) {
  try {
    const response = await fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        [category]: value
      })
    });
    return await response.json();
  } catch (error) {
    console.log('Error', error);
  }
}

async function sendMail(emailsView) {
  try {
    const response = fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    const data = await response.json();
    console.log(data);
    loadMail('sent', emailsView);
  } catch (error) {
    console.log('Error:', error);
    return false;
  }
}