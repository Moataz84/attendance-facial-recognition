const socket = io()

function signout(e) {
  e.preventDefault()
  const person = e.target.parentElement
  const id = person.getAttribute("data-id")
  person.querySelector(".time").remove()
  person.querySelector(".cover").classList.remove("hidden")
  const btn = person.querySelector("button")
  btn.textContent = "Sign In"
  btn.setAttribute("onclick", "signin(event)")
  socket.emit("signout", id)
}

function signin(e) {
  e.preventDefault()
  const person = e.target.parentElement
  const id = person.getAttribute("data-id")
  socket.emit("check-present", id)
}