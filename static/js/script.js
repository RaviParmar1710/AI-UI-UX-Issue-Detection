const fileInput = document.getElementById("fileInput");
const previewImage = document.getElementById("previewImage");
const form = document.querySelector("form");

fileInput.addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      previewImage.src = e.target.result;
      previewImage.style.display = "block";
    };
    reader.readAsDataURL(file);
  } else {
    previewImage.style.display = "none";
  }
});

// Optional: Prevent submission if no image is selected
form.addEventListener("submit", function (e) {
  if (!fileInput.files.length) {
    alert("Please upload an image before submitting.");
    e.preventDefault();
  }
});
