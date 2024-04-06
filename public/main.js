const video = document.querySelector("video")
const socket = io()
let videoId = null

socket.on("connect", () => socket.emit("get-video-id"))

window.addEventListener("beforeunload", () => socket.emit("disconnect-client", videoId))

socket.on("video-id", id => {
  videoId = id
})

function captureFrame() {
  const canvas = document.createElement("canvas")
  const context = canvas.getContext("2d")
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  context.drawImage(video, 0, 0, canvas.width, canvas.height)
  const imgData = canvas.toDataURL("image/jpeg", 0.8)
  return imgData
}

navigator.mediaDevices.getUserMedia({
  audio: false, 
  video: true
}).then(async stream => {
  videoTracks = stream.getVideoTracks()
  video.srcObject = stream
  setInterval(() => {
    socket.emit("frame", {videoId, frame: captureFrame()})
  }, 33)  
})

