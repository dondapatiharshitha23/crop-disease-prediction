const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const captureButton = document.getElementById("capture");
const sendButton = document.getElementById("send");
const preview = document.getElementById("preview");
const resultBox = document.getElementById("result-box");
const resultText = document.getElementById("result-text");
// Access the webcam
navigator.mediaDevices
.getUserMedia({ video: true })
.then((stream) => {
video.srcObject = stream;
})
.catch((err) => {
console.error("Error accessing the webcam: ", err);
});
// Capture the photo
captureButton.addEventListener("click", () => {
  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  // Get the image as data URL and show preview
  const imageData = canvas.toDataURL("image/png");
  preview.src = imageData;
  preview.style.display = "block";
  sendButton.style.display = "block";
});
// Send the photo for prediction
sendButton.addEventListener("click", () => {
const category = document.querySelector('input[name="category"]:checked').value;
const imageData = canvas.toDataURL("image/png");
const endpoint =
category === "tomato"
? "/predicttomatodisesase"
: "/predictchillidisesase";
fetch(endpoint, {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify({ image: imageData }),
})
.then((response) => response.json())
.then((data) => {
// Display the result in the result box
resultBox.style.display = "block";
resultText.textContent = data.message;
})
.catch((error) => {
console.error("Error:", error);
resultBox.style.display = "block";
resultText.textContent = "An error occurred. Please try again.";
});
})