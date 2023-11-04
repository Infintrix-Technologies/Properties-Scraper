// Get the modal and image elements
const imagePreviewModal = document.querySelector(".modal");
const modalImage = document.querySelector(".modal-property-image");
const propertyImages = document.querySelectorAll(".property-image");

// Function to open the modal when a property image is clicked
propertyImages.forEach((img) => {
  img.addEventListener("click", () => {
    imagePreviewModal.style.display = "block";
    modalImage.src = img.src;
  });
});

// Function to close the modal when the close button is clicked
const closeBtn = document.querySelector(".close");
closeBtn.addEventListener("click", () => {
  imagePreviewModal.style.display = "none";
});

// --------------------------------------

// Get references to the modal and close button
const notesModal = document.querySelector(".notes-modal");
const closeModal = document.querySelector(".notes-close");

// Get all notesButton with the "notes-btn" class
const notesButton = document.querySelectorAll(".notes-btn");

// Add click event listeners to each button
notesButton.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    const propertyId = e.target.getAttribute("property-id");
    // /api/rightmove/properties/1673/notes/
    fetch(`/api/rightmove/properties/${propertyId}/notes/`)
      .then((response) => response.json())
      .then((data) => {
        // Check if data is an array
        if (Array.isArray(data) && data.length > 0) {
          // Clear any previous notes in the modal
          const notesContent = document.getElementById("notes-content");
          notesContent.innerHTML = "";

          // Create an unordered list for displaying notes
          const ul = document.createElement("ul");

          data.forEach((note) => {
            // Create a list item for each note
            const li = document.createElement("li");
            li.textContent = note.text;
            ul.appendChild(li);
          });

          // Append the list to the modal
          notesContent.appendChild(ul);

          // Display the modal
          modal.style.display = "block";
        } else {
          // If no notes data is available, display a message
          const notesContent = document.getElementById("notes-content");
          notesContent.innerHTML = "No notes available.";
          modal.style.display = "block";
        }
      })
      .catch((error) => {
        console.error("Error fetching notes:", error);
      });
    notesModal.style.display = "block";
  });
});

// Add click event listener to the close button
closeModal.addEventListener("click", () => {
  notesModal.style.display = "none";
});
