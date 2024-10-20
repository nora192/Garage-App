document.getElementById('bookingForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    // Get start and end time values from the form
    const startTime = document.querySelector('.start-time').value;
    const endTime = document.querySelector('.end-time').value;

    // Validate times before proceeding with the AJAX request
    if (!validateTimes(startTime, endTime)) {
        const errorContainer = document.getElementById('error-message');
        errorContainer.textContent = "End time must be after start time.";
        errorContainer.style.display = "block";
        return; 
    }

    const formData = new FormData(this);

    // Proceed with AJAX request only if times are valid
    fetch('/edit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert(data.message);
            window.location.href = "/profile";  
        } else {
            const errorContainer = document.getElementById('error-message');
            errorContainer.textContent = data.message;
            errorContainer.style.display = "block";
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

// Function to validate start and end times
function validateTimes(start, end) {
    const [startHours, startMinutes] = start.split(':').map(Number);
    const [endHours, endMinutes] = end.split(':').map(Number);

    const startTime = new Date();
    startTime.setHours(startHours, startMinutes);

    const endTime = new Date();
    endTime.setHours(endHours, endMinutes);

    return endTime > startTime;
}
