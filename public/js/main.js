const socket = io()

socket.on("show-person", id => {
  const person = document.querySelector(`[data-id="${id}"]`)
  person.querySelector(".cover").classList.add("hidden")

  const btn = person.querySelector("button")
  if (!btn) return
  person.insertAdjacentHTML(
    "beforeend", `<p class="time">Present at: ${new Date().toLocaleTimeString([], {timeStyle: "short"})}</p>`
  )
  btn.textContent = "Sign Out"
  btn.setAttribute("onclick", "signout(event)")
})

function signin(e) {
  const person = e.target.parentElement
  const id = person.getAttribute("data-id")
  socket.emit("check-present", id)
}

function signoutPerson(person) {
  person.querySelector(".time").remove()
  person.querySelector(".cover").classList.remove("hidden")
  const btn = person.querySelector("button")
  btn.textContent = "Sign In"
  btn.setAttribute("onclick", "signin(event)")
}

function signout(e) {
  const person = e.target.parentElement
  const id = person.getAttribute("data-id")
  signoutPerson(person)
  socket.emit("signout", id)
}

function signAllOut() {
  const people = [...document.querySelectorAll(".person")]
  for (let person of people) {
    if (person.children[0].classList.contains("hidden")) {
      signoutPerson(person)
      socket.emit("signout-all")
    }
  }
}

socket.on("signedout", id => {
  const person = document.querySelector(`[data-id="${id}"]`)
  person.querySelector(".cover").classList.remove("hidden")
})

socket.on("signedout-all", () => {
  const people = [...document.querySelectorAll(".person")]
  for (let person of people) {
    person.querySelector(".cover").classList.remove("hidden")
  }
})