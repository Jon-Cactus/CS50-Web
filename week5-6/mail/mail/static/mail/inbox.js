document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => {
    loadMailbox('inbox');
  });
  document.querySelector('#sent').addEventListener('click', () => {
    loadMailbox('sent');
  });
  document.querySelector('#archived').addEventListener('click', () => {
    loadMailbox('archive');
  });
  document.querySelector('#compose').addEventListener('click', composeEmail);
  // Send Mail
  document.querySelector('#compose-form').onsubmit = sendMail; 

  // By default, load the inbox
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
const loadMail = (mailType) => {
  
  const emailsView = document.getElementById('emails-view');
  emailsView.innerHTML = '';
  fetch(`/emails/${mailType}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      const emailPreviewDiv = document.createElement('div');
      // TODO: depending on the mail's status, change which class is added
      emailPreviewDiv.innerHTML = `
      <span><strong>${email.sender}</strong></span>
      <span>${email.subject}</span>
      <span>${email.timestamp}</span>
      `;

      // Add 'read' class if the email in the inbox and has been opened
      if (mailType === 'inbox' && email.read === true) {
        emailPreviewDiv.classList.add('read');
      }
      emailPreviewDiv.classList.add('email-preview');
      emailPreviewDiv.dataset.id = email.id; // set id in the element's dataset
      emailsView.append(emailPreviewDiv);
    })
    .catch(error => console.log('Error', error));
  })

  // Add event listener to the parent element of the email previews that listens for clicks
  emailsView.addEventListener('click', (event) => {
    const emailId = event.target.closest('.email-preview').dataset.id; // find id value of clicked email
    fetch(`/emails/${emailId}`) 
    .then(response => response.json())
    .then(email => {

      // Render mail
      const emailView = document.getElementById('email-view')
      const emailDiv = document.createElement('div');
      emailView.style.display = 'block';
      emailsView.style.display = 'none';
      emailView.innerHTML = ''; // Clear any previously loaded emails
      emailDiv.innerHTML = `
        <p><strong>From: </strong>${email.sender}</p>
        <p><strong>To: </strong>${email.recipients}</p>
        <p><strong>Subject: </strong>${email.subject}</p>
        <p><strong>Timestamp: </strong>${email.timestamp}</p>
        <hr></hr>
        <p>${email.body}</p>
      `;
      // Add proper buttons and event listeners to update the email's status
      if (mailType === 'inbox') {
        emailDiv.innerHTML += `
        <div>
          <button class="btn btn-sm btn-outline-primary" id="unread">Mark as unread</button>
          <button class="btn btn-sm btn-outline-primary" id="archive">Archive</button>
        </div>
        `
        emailView.append(emailDiv);
        document.getElementById('unread').addEventListener('click', () => {
          updateMailStatus(emailId, "read", false);
        });
        document.getElementById('archive').addEventListener('click', () => {
          updateMailStatus(emailId, "archived", true);
          loadMailbox('inbox');
        });
      } else if (mailType === 'archive') {
          emailDiv.innerHTML += '<button class="btn btn-sm btn-outline-primary" id="unarchive">Unarchive</button>'
          emailView.append(emailDiv);
          document.getElementById('unarchive').addEventListener('click', () => {
          updateMailStatus(emailId, "archived", false);
          loadMailbox('inbox');
        });
      }
    })
    .catch(error => console.log('Error', error));
    updateMailStatus(emailId, "read", true); // Change mail to read
  });
}

const updateMailStatus = (id, category, value) => {

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      [category]: value
    })
  })
  .then(() => {
    loadMailbox('inbox');
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
  .catch(error => {
    console.log('Error:', error);
  });

 
  return false;
}

function loadMailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Load all mail in a given mailbox
  loadMail(mailbox);

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}