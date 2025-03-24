document.addEventListener('DOMContentLoaded', function() {
  const emailView = document.getElementById('email-view');
  const composeView = document.getElementById('compose-view');
  const emailsView = document.getElementById('emails-view');


  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => loadMailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => loadMailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => loadMailbox('archive'));
  document.querySelector('#compose').addEventListener('click', composeEmail);
  document.querySelector('#compose-form').onsubmit = sendMail; // Send Mail

  // Add event listener for email clicks once
    emailsView.addEventListener('click', (event) => {
      const emailPreview = event.target.closest('.email-preview');
      if (emailPreview) {
        const emailId = emailPreview.dataset.id;
        const mailbox = emailsView.dataset.mailbox; // Get current mailbox type
        fetch(`/emails/${emailId}`)
          .then(response => response.json())
          .then(email => {
            // Render email
            emailView.style.display = 'block';
            emailsView.style.display = 'none';
            composeView.style.display = 'none';
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
                  <button class="btn btn-sm btn-outline-primary" id="unread">Mark as unread</button>
                  <button class="btn btn-sm btn-outline-primary" id="archive">Archive</button>
                </div>
              `;
            } else if (mailbox === 'archive') {
              emailDiv.innerHTML += '<button class="btn btn-sm btn-outline-primary" id="unarchive">Unarchive</button>';
            }
            emailView.append(emailDiv);
  
            // Add event listeners to buttons
            if (mailbox === 'inbox') {
              document.getElementById('unread').addEventListener('click', () => {
                updateMailStatus(emailId, "read", false);
              });
              document.getElementById('archive').addEventListener('click', () => {
                updateMailStatus(emailId, "archived", true)
                  .then(() => loadMailbox('inbox'));
              });
            } else if (mailbox === 'archive') {
              document.getElementById('unarchive').addEventListener('click', () => {
                updateMailStatus(emailId, "archived", false)
                  .then(() => loadMailbox('inbox'));
              });
            }
          })
          .catch(error => console.log('Error', error));
        if (mailbox === 'inbox') {
          updateMailStatus(emailId, "read", true); // Mark as read only for inbox
        }
      }
    });
    loadMailbox('inbox');
  });

function composeEmail() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// Loads mail in the appropriate mailbox
const loadMail = (mailbox, emailsView) => {
  emailsView.innerHTML = '';
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      const emailPreviewDiv = document.createElement('div');
      emailPreviewDiv.innerHTML = `
      <span><strong>${email.sender}</strong></span>
      <span>${email.subject}</span>
      <span>${email.timestamp}</span>
      `;
      // Add 'read' class if the email in the inbox and has been opened
      if (mailbox === 'inbox' && email.read) {
        emailPreviewDiv.classList.add('read');
      }
      emailPreviewDiv.classList.add('email-preview');
      emailPreviewDiv.dataset.id = email.id; // set id in the element's dataset
      emailsView.append(emailPreviewDiv);
    })
  })
  .catch(error => console.log('Error', error));
}

// After many issues and searching, it turned out that the only way I could find to solve my
// issue of not seeing 'read' or 'archived' status changes immediately following clicking a the mail,
// 'unread' button, 'archive' button, or 'unarchive' button, 
// was by implementing an asynchronous function here
const updateMailStatus = (id, category, value) => {
  return fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      [category]: value
    })
  })
  .catch(error => console.log('Error', error));
}

const sendMail = () => {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result)
    loadMailbox('sent');
  })
  .catch(error => console.log('Error:', error));
  return false;
}

function loadMailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  const emailsView = document.getElementById('emails-view');
  // Show the mailbox name
  emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  emailsView.dataset.mailbox = mailbox; // This was the only way I could properly add the correct eventlistener

  // Load all mail in a given mailbox
  loadMail(mailbox, emailsView);
}