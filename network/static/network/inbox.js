document.addEventListener('DOMContentLoaded', function() {
  likeFunction(this);
  subscribeFunction(this);
  editPost(this);
  confitmPost(this);
})

function likeFunction(button) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  const postID = button.dataset.post_id

  fetch('/like/' + postID, {
    headers: {'X-CSRFToken': csrftoken},
    method: 'PUT',
  })
  .then(() => {
    if (button.dataset.pressed == 'false') {
      document.querySelector(`.likeCount-${postID}`).innerHTML++
      button.dataset.pressed = 'true'
      button.innerHTML =
        "<svg width ='24' height = '24'<g><path d='M3,11h3v10H3V11z M18.77,11h-4.23l1.52-4.94C16.38,5.03,15.54,4,14.38,4c-0.58,0-1.14,0.24-1.52,0.65L7,11v10h10.43 c1.06,0,1.98-0.67,2.19-1.61l1.34-6C21.23,12.15,20.18,11,18.77,11z'></path> </g> </svg>"
    } else {
      document.querySelector(`.likeCount-${postID}`).innerHTML--
      button.dataset.pressed = 'false'
      button.innerHTML =
        "<svg width = '24' height = '24'><g><path d='M18.77,11h-4.23l1.52-4.94C16.38,5.03,15.54,4,14.38,4c-0.58,0-1.14,0.24-1.52,0.65L7,11H3v10h4h1h9.43 c1.06,0,1.98-0.67,2.19-1.61l1.34-6C21.23,12.15,20.18,11,18.77,11z M7,20H4v-8h3V20z M19.98,13.17l-1.34,6 C18.54,19.65,18.03,20,17.43,20H8v-8.61l5.6-6.06C13.79,5.12,14.08,5,14.38,5c0.26,0,0.5,0.11,0.63,0.3 c0.07,0.1,0.15,0.26,0.09,0.47l-1.52,4.94L13.18,12h1.35h4.23c0.41,0,0.8,0.17,1.03,0.46C19.92,12.61,20.05,12.86,19.98,13.17z'> </path> </g> </svg>"
    }
  })
}

function subscribeFunction(button) {
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value
  const author = button.dataset.author

  fetch('/subscribe/' + author, {
    headers: {'X-CSRFToken': csrftoken},
    method: 'PUT',
  })
  .then(() => {
    if (button.dataset.substatus == 'false') {
      document.querySelectorAll(`button[data-author="${author}"]`).forEach(button => {
        button.dataset.substatus = "true"
        button.title = "unsubscribe"
        button.innerHTML =
          "<img src='/static/network/black.png' class='imagepad' width='18px' height='18px'>"
      })
      document.querySelector('.changefw').innerHTML++
    } else {
      document.querySelectorAll(`button[data-author="${author}"]`).forEach(button => {
        button.dataset.substatus = "false"
        button.title = "subscribe"
        button.innerHTML =
          "<img src='/static/network/white.png' class='imagepad' width='18px' height='18px'>"
      })
      document.querySelector('.changefw').innerHTML--
    } 
  })
}

function editPost(button) {
  document.querySelectorAll('.editButton').forEach(button => {
    button.style.display = 'none'
  })

  const postID = button.dataset.post_id
  const postArea = document.querySelector(`.postArea-${postID}`)
  const divPostArea = document.querySelector(`.divPostArea-${postID}`)

  postArea.style.display = 'none'

  const newTextArea = document.createElement('textarea')
  newTextArea.setAttribute("class", `editTextArea editTextArea-${postID}`)
  const text = postArea.innerHTML.trim()
  newTextArea.value = text
  divPostArea.append(newTextArea)

  const confirmButton = document.createElement('button')
  confirmButton.setAttribute('class', 'confirmButton')
  confirmButton.setAttribute('onclick', 'confirmPost(this)')
  confirmButton.setAttribute('data-post_id', `${postID}`)
  confirmButton.innerText = 'confirm'

  const divBut = document.querySelector(`.divBut-${postID}`)
  divBut.append(confirmButton)
}

function confirmPost(button) {
   const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value
   const postID = button.dataset.post_id
   const redactedText = document.querySelector(`.editTextArea-${postID}`)
   const data = {body: redactedText.value}

   fetch('/editpost/'+postID, {
    headers: {'X-CSRFToken': csrftoken},
    method: 'PUT',
    body: JSON.stringify(data),
   }) 
   .then(() => {
    removeOld('.confirmButton')
    removeOld(`.editTextArea-${postID}`)
    document.querySelectorAll('.editButton').forEach(button => {
      button.style.display = 'block'
    })
    const postArea = document.querySelector(`.postArea-${postID}`)
    if (redactedText.value.length == 0) 
    removeOld(`.comment-${postID}`)
    else 
    postArea.style.display = 'block'
    postArea.innerText = redactedText.value
   })
}

function removeOld(element) {
  const old = document.querySelector(element)
  old.remove()
}