document.addEventListener("DOMContentLoaded", function () {
    const calendarDays = document.querySelectorAll(".clickable-day");
    const detailsContainer = document.getElementById("day-details");
    const dayTitle = document.getElementById("day-title");
    const dayInfo = document.getElementById("day-info");

    calendarDays.forEach(day => {
        day.addEventListener("click", function () {
            let date = this.getAttribute("data-date");

            if (date) {
                fetch(`/get-day-details/?date=${date}`)
                    .then(response => response.json())
                    .then(data => {
                        // Set title and info
                        dayTitle.innerText = `Opening Details for ${data.date}`;

                        if (data.status === "open") {
                            dayInfo.innerHTML = `<strong>Opening Hours:</strong> ${data.opening_time} - ${data.closing_time}`;
                        } else if (data.status === "closed") {
                            dayInfo.innerHTML = `<strong>Closed:</strong> ${data.reason}`;
                        } else {
                            dayInfo.innerHTML = `<strong>No data available for this day.</strong>`;
                        }

                        // Show the card
                        detailsContainer.classList.add("show");
                    })
                    .catch(error => console.error("Error fetching day details:", error));
            }
        });
    });
});
