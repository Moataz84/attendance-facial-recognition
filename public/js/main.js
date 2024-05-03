const socket = io()

socket.on("show-person", id => {
  if (window.location.pathname !== "/") return
  const person = document.querySelector(`[data-id="${id}"]`)
  person.insertAdjacentHTML(
    "beforeend", `<p class="time">Present at: ${new Date().toLocaleTimeString([], {timeStyle: "short"})}</p>`
  )
  person.querySelector(".cover").classList.add("hidden")
  const btn = person.querySelector("button")
  btn.textContent = "Sign Out"
  btn.setAttribute("onclick", "signout(event)")
})

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