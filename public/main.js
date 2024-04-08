const video = document.querySelector("video")
const socket = io()
let imageId = interval = null
let connected = false

socket.on("connect", () => {
  imageId = socket.id
  connected = true
})

window.addEventListener("beforeunload", () => {
  connected = false
  clearInterval(interval)
  socket.emit("disconnect-client", imageId)
})

socket.on("face-result", name => {
  document.querySelector("p").innerText = name
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

navigator.mediaDevices.getUserMedia({
  audio: false, 
  video: true
}).then(async stream => {
  videoTracks = stream.getVideoTracks()
  video.srcObject = stream
  interval = setInterval(() => {
    if (connected) socket.emit("frame", {imageId, frame: captureFrame()})
  }, 50)
})