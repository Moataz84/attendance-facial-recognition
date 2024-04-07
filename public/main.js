const video = document.querySelector("video")
const socket = io()
let imageId = null

socket.on("connect", () => socket.emit("get-image-id"))

window.addEventListener("beforeunload", () => socket.emit("disconnect-client", imageId))

socket.on("image-id", id => {
  imageId = id
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
  setInterval(() => {
    if (socket.connected) socket.emit("frame", {imageId, frame: captureFrame()})
  }, 50)  
})