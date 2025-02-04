document.addEventListener("DOMContentLoaded", function () {
    // Select all calendar day cells
    const calendarDays = document.querySelectorAll(".calendar td");

    calendarDays.forEach(day => {
        day.addEventListener("click", function () {
            let date = this.getAttribute("data-date");

            if (date) {
                fetch(`/get-day-details/?date=${date}`)
                    .then(response => response.json())
                    .then(data => {
                        let message = "";

                        if (data.status === "open") {
                            message = `Opening Hours: ${data.opening_time} - ${data.closing_time}`;
                        } else if (data.status === "closed") {
                            message = `Closed: ${data.reason}`;
                        } else {
                            message = "No data available for this day.";
                        }

                        alert(`${data.date}: ${message}`);
                    })
                    .catch(error => {
                        console.error("Error fetching day details:", error);
                    });
            }
        });
    });
});
