document.addEventListener("DOMContentLoaded", function () {
    const uploadForm = document.getElementById("upload-form");
    const uploadButton = document.getElementById("upload-button");
    const uploadStatus = document.getElementById("upload-status");

    uploadForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const imageInput = document.getElementById("imageInput");
        const formData = new FormData(uploadForm);

        fetch("/upload", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                uploadStatus.textContent = "Image uploaded and saved successfully!";
                uploadStatus.style.backgroundColor = "#27ae60";
                uploadStatus.classList.remove("hidden");
                imageInput.value = "";

                // Redirect to /attendance after a successful upload
                window.location.href = "/attendance";
            } else {
                uploadStatus.textContent = "Image upload failed. Please try again.";
                uploadStatus.style.backgroundColor = "#e74c3c";
                uploadStatus.classList.remove("hidden");
            }
        });
    });
});