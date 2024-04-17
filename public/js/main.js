const socket = io()

socket.on("show-person", person => {
  console.log(person)
})