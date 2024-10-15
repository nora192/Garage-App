document.getElementById('book-range').addEventListener('click', function(event) {
    const startTime = document.getElementById('start-time').value;
    const endTime = document.getElementById('end-time').value;

    if (!validateTimes(startTime, endTime)) {
        alert("End time must be after start time.");
        event.preventDefault(); 
        return; 
    }
    
    checkUnavailableSlots(startTime, endTime, function(available){
        if(available){
            window.location.href = "/book-slot/{{ slot['slot_id'] }}/{{ date }}/" + startTime + "/" + endTime;
        }

        else{
            alert("Some hours in the selected range are unavailable.");
            event.preventDefault();
        }
    }); 

    function checkUnavailableSlots(start, end, callback){
        const xhr = new XMLHttpRequest();
        const date = document.getElementById("slot-times").getAttribute("date");
        const slot_id = document.getElementById("slot-times").getAttribute("slot_id");
        console.log(date);
        xhr.open("Get", `/check-range?start=${start}&end=${end}&date=${date}&slot_id=${slot_id}`, true);

        xhr.onreadystatechange = function(){
            if(xhr.readyState == 4 && xhr.status == 200){
                var response = JSON.parse(xhr.responseText);
                callback(response.available);
            }
        };
        xhr.send();

    }

    function validateTimes(start, end) {
        // Convert times to Date objects for comparison
        const [startHours, startMinutes] = start.split(':').map(Number);
        const [endHours, endMinutes] = end.split(':').map(Number);

        const startTime = new Date();
        startTime.setHours(startHours, startMinutes);

        const endTime = new Date();
        endTime.setHours(endHours, endMinutes);
        return endTime > startTime;
    }
    
});
