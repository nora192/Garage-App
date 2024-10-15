
document.addEventListener("DOMContentLoaded", function() {
    const categoryFilter = document.getElementById("category-filter");
    const priceFilter = document.getElementById("price-filter");
    const priceValue = document.getElementById("price-value");

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

    dateFilter.addEventListener("input", filterSlotCards);



    function filterSlotCards(){
        const categorySelected = categoryFilter.value;
        const maxPrice = priceFilter.value;
        const date = new Date(dateFilter.value);
        const formattedDate = date.toISOString().split('T')[0];

        const xhr = new XMLHttpRequest();
        xhr.open("Get", `/filter-slots?category=${categorySelected}&price_per_hour=${maxPrice}&date=${formattedDate}`, true);

        xhr.onreadystatechange = function(){
            if(xhr.readyState == 4 && xhr.status == 200){
                const slotsContainer = document.getElementById("slots-container");
                const response = JSON.parse(xhr.responseText);

                slotsContainer.innerHTML = '';
                response.forEach(slot => {

                    const soltElement = 
                    `
                        <article class="card">
                            <h4>Slot ${slot.slot_id} - ${slot.location}</h4>
                            <p>Slot Category : ${slot.category}</p>
                            <p>Price per hour: ${ slot.price_per_hour}</p>
                            
                            
                            <div class="availability-time">
                                <a href="/slot-details/${slot.slot_id}?date=${formattedDate}">see when this slot is available</a>
                                <a href="/slot-details/${slot.slot_id}?date=${formattedDate}">
                                    <i class="fas fa-long-arrow-alt-right" ></i>
                                </a>
                            </div>
                            
                            
                        </article>
                    `;
                    slotsContainer.insertAdjacentHTML('beforeend', soltElement);
                    
                });

            }
        };
        xhr.send();

    }

});

