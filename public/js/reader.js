const video = document.querySelector("video")
const p = document.querySelector("p")
const socket = io()
let imageId = interval = null
let connected = false
let disconnecting = false
let ids = []

socket.on("connect", () => {
  imageId = socket.id
  connected = true
})

window.addEventListener("beforeunload", () => {
  disconnecting = true
  connected = false
  socket.emit("disconnect-client", imageId)
})

socket.on("face-result", data => {
  connected = true
  const { id, name } = data
  p.innerText = ""
  if (!id) p.innerText = name
  if (ids[ids.length - 1] === id || ids.length === 0) {
    ids.push(id)
    if (ids.length === 5) {
      ids = []
      socket.emit("check-present", id)
    }
  }
  if (!id) ids = []
})

socket.on("mark-present", person => {
  p.innerText = `${person.name} is present`
  clearInterval(interval)
  setTimeout(() => {
    p.innerText = ""
    interval = setInterval(sendFrame, 50)
  }, 3000)
})

function captureFrame() {
  const canvas = document.createElement("canvas")
  const context = canvas.getContext("2d")
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  context.drawImage(video, 0, 0, canvas.width, canvas.height)
  const imgData = canvas.toDataURL("image/jpeg", 1)
  return imgData
}

function sendFrame() {
  if (disconnecting) clearInterval(interval)
  if (connected && !disconnecting) socket.emit("frame", {imageId, frame: captureFrame()})
  connected = false
}

navigator.mediaDevices.getUserMedia({
  audio: false, 
  video: true
}).then(async stream => {
  videoTracks = stream.getVideoTracks()
  video.srcObject = stream
  interval = setInterval(sendFrame, 50)
})