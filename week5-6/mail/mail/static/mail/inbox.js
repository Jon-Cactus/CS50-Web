document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => {
    load_mailbox('inbox');
    load_mail('inbox');

    
  });
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // Send Mail
  document.querySelector('#compose-form').onsubmit = send_mail; 

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// Loads mail in the appropriate mailbox
const load_mail = (mailType) => {
  
  const inbox = document.getElementById('emails-view');
  fetch(`/emails/${mailType}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      const emailDiv = document.createElement('div');
      // TODO: clean this up
      emailDiv.innerHTML = `
      <span><strong>${email.sender}</strong></span>
      <span>${email.subject}</span>
      <span>${email.timestamp}</span>
      `;
      emailDiv.classList.add('email-preview');
      emailDiv.dataset.id = email.id;
      inbox.append(emailDiv);
    })
  })

  inbox.addEventListener('click', (event) => { // event listener for each email
    fetch(`/emails/${event.target.closest('.email-preview').dataset.id}`) // find id value of clicked email
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // TODO: render mail here
    })
    
  });
}




const send_mail = () => {

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
    load_mailbox('sent');
  })
  .catch(error => {
    console.log('Error:', error);
  });

 
  return false;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}