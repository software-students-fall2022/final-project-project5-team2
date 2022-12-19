// Set constraints for the video stream
var constraints = { video: { facingMode: "user" }, audio: false }; // Define constants
const cameraView = document.querySelector("#camera--view"),
  cameraOutput = document.querySelector("#camera--output"),
  cameraSensor = document.querySelector("#camera--sensor"),
  cameraTrigger = document.querySelector("#camera--trigger"); // Access the device camera and stream to cameraView
const cameraSubmit = document.querySelector("#camera--submit");
function cameraStart() {
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(function (stream) {
      track = stream.getTracks()[0];
      cameraView.srcObject = stream;
    })
    .catch(function (error) {
      console.error("Oops. Something is broken.", error);
    });
} // Take a picture when cameraTrigger is tapped
cameraTrigger.onclick = function (e) {
  e.preventDefault();
  cameraSensor.width = cameraView.videoWidth;
  cameraSensor.height = cameraView.videoHeight;
  cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);
  cameraOutput.src = cameraSensor.toDataURL("image/png");
  cameraOutput.classList.add("taken");

  cameraView.style = "display:none;";
  cameraTrigger.style = "display:none;";
  cameraSubmit.style = "display:block;";

  document.getElementById("retry").style = "display: none;";

  document.getElementById("opImage").value = cameraOutput.src;
}; // Start the video stream when the window loads
window.addEventListener("load", cameraStart, false);
