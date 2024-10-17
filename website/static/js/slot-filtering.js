document.addEventListener("DOMContentLoaded", function() {
    const categoryFilter = document.getElementById("category-filter");
    const priceFilter = document.getElementById("price-filter");
    const priceValue = document.getElementById("price-value");

    // Set today's date as the default date
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    document.getElementById("date").value = formattedDate;

    const dateFilter = document.getElementById("date");

    // Update price value display
    priceFilter.addEventListener("input", function() {
        priceValue.textContent = priceFilter.value;
        filterSlotCards();
    });

    // Apply filters when the category filter changes
    categoryFilter.addEventListener("change", filterSlotCards);

    // Apply filters when the date changes
    dateFilter.addEventListener("input", filterSlotCards);

    // Function to filter the slots based on category, price, and date
    function filterSlotCards(){
        const categorySelected = categoryFilter.value;
        const maxPrice = priceFilter.value;
        const date = new Date(dateFilter.value);
        const formattedDate = date.toISOString().split('T')[0];

        const xhr = new XMLHttpRequest();
        xhr.open("GET", `/filter-slots?category=${categorySelected}&price_per_hour=${maxPrice}&date=${formattedDate}`, true);

        xhr.onreadystatechange = function(){
            if(xhr.readyState == 4 && xhr.status == 200){
                const slotsContainer = document.getElementById("slots-container");
                const response = JSON.parse(xhr.responseText);

                slotsContainer.innerHTML = '';

                response.forEach(slot => {
                    let startTimeOptions = '';
                    let endTimeOptions = '';
                    if (Array.isArray(slot.available_times)) {
                        slot.available_times.forEach(time => {
                            startTimeOptions += `<option value="${time}">${time}</option>`;
                            endTimeOptions += `<option value="${time}">${time}</option>`;
                        });
                    } else {
                        startTimeOptions = '<option value="">No available times</option>';
                        endTimeOptions = '<option value="">No available times</option>';
                    }

                    const slotElement = `
                        <article class="card">
                            <h4 id="location">${slot.location}</h4>
                            <p id="category">Slot Category: ${slot.category}</p>
                            <p>Price per hour: $${slot.price_per_hour}</p>
                            
                            <div class="time-range-selection">
                                <label for="start-time">Select Start Time:</label>
                                <select class="start-time" name="start-time">
                                    ${startTimeOptions}
                                </select>
                            
                                <label for="end-time">Select End Time:</label>
                                <select class="end-time" name="end-time">
                                    ${endTimeOptions}
                                </select>
                            
                                <a href="#" class="btn btn-primary book-range" data-slot="${slot.location}">Book Now</a>
                            </div>
                        </article>
                    `;
                    slotsContainer.insertAdjacentHTML('beforeend', slotElement);
                });

                // Re-attach date-time filter for newly loaded slots
                dateTimeFilter();
            }
        };
        xhr.send();
    }

    // Function to handle booking time range validation and availability check
    function dateTimeFilter(){
        document.querySelectorAll('.book-range').forEach(function(button) {
            button.addEventListener('click', function(event) {
                const container = event.target.closest('.time-range-selection');
                const startTime = container.querySelector('.start-time').value;
                const endTime = container.querySelector('.end-time').value;
                const location = container.closest('article').querySelector('h4').innerText;
                const date = document.getElementById("date").value;
        
                if (!validateTimes(startTime, endTime)) {
                    alert("End time must be after start time.");
                    event.preventDefault(); 
                    return; 
                }
        
                checkUnavailableSlots(startTime, endTime, location, date, function(available){
                    if(available){
                        console.log("available");
                        // window.location.href = `/book-slot/${location}/${date}/${startTime}/${endTime}`;
                    } else {
                        alert("Some hours in the selected range are unavailable.");
                        event.preventDefault();
                    }
                });
            });
        });
    }

    // Function to check the availability of the selected time range
    function checkUnavailableSlots(start, end, location, date, callback) {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", `/check-range?start=${start}&end=${end}&date=${date}&slot_location=${location}`, true);
        
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                const response = JSON.parse(xhr.responseText);
                callback(response.available);
            }
        };
        xhr.send();
    }

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

    // Initial load of slot cards
    filterSlotCards();
});
