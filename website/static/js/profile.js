document.addEventListener("DOMContentLoaded", function() {
    const dateElements = document.getElementsByClassName("date");
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    const timeNow = today.getHours(); // current hour

    // Iterate over all date elements and check if date is today or past
    for (let i = 0; i < dateElements.length; i++) {
        const dateValue = dateElements[i].textContent.trim();

        // Find the closest reserved slot element
        const reservedSlot = dateElements[i].closest('.reserved-slot');
        const btns = reservedSlot.getElementsByClassName("btns");

        // Access data attributes for the slot details
        const location = reservedSlot.dataset.location;
        const start = reservedSlot.dataset.start;
        const end = reservedSlot.dataset.end;
        const slotDate = reservedSlot.dataset.date;

        // For past dates, disable the edit and cancel buttons
        if (dateValue < formattedDate) {
            for (let btn of btns) {
                btn.style.display = "none";
                btn.insertAdjacentHTML('afterend', 
                    `<a href="/cancel-booking?location=${location}&start=${start}&end=${end}&date=${slotDate}">Out of date, click to remove</a>`
                );
            }
        }
        // If the date is today, compare the time
        else if (dateValue === formattedDate) {

            const endElement = reservedSlot.getElementsByClassName("end")[0]; // Get the 'end' element within the same card
            const endTime = parseInt(endElement.getAttribute("data-end-time"));

            // If the current time is past the end time, disable the buttons
            if (timeNow >= endTime) {
                for (let btn of btns) {
                    btn.style.display = "none";
                    btn.insertAdjacentHTML('afterend', 
                        `<a href="/cancel-booking?location=${location}&start=${start}&end=${end}&date=${slotDate}">Out of date, click to remove</a>`
                    );
                }
            }
        }
        // For future dates, do nothing
        else {
            continue;
        }
    }
});
