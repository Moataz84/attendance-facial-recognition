const socket = io()

socket.on("show-person", person => {
  document.querySelector(".present").insertAdjacentHTML(
    "beforeend",
    `<div class="person" data-id="${person.id}">
    <img src="public/imgs/${person.profile}">
    <p>${person.name}</p>
    <button onclick="signout(event)">Sign Out</button>
    </div>`
  )
})

function signout(e) {
  e.preventDefault()
  const id = e.target.parentElement.getAttribute("data-id")
  document.querySelector(`[data-id="${id}"]`).remove()
  socket.emit("signout", id)
}