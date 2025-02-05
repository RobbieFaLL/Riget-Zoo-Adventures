document.addEventListener("DOMContentLoaded", function () {
    const calendarDays = document.querySelectorAll(".clickable-day");
    const modal = document.getElementById("day-modal");
    const modalTitle = document.getElementById("modal-title");
    const modalContent = document.getElementById("modal-content");
    const modalClose = document.getElementById("modal-close");

    calendarDays.forEach(day => {
        day.addEventListener("click", function () {
            let date = this.getAttribute("data-date");

            if (date) {
                fetch(`/get-day-details/?date=${date}`)
                    .then(response => response.json())
                    .then(data => {
                        modalTitle.innerText = `${new Date(date).toLocaleDateString("en-GB", { day: 'numeric', month: 'long' })} Opening Times`;

                        if (data.opening_time && data.closing_time) {
                            modalContent.innerHTML = `
                                <p><strong>Opening Hours:</strong> ${data.opening_time} - ${data.closing_time}</p>
                                <a href="/booking/" class="book-btn">Book Now</a>
                            `;
                        } else if (data.reason) { 
                            modalContent.innerHTML = `<p><strong>Closed:</strong> ${data.reason}</p>`;
                        } else {
                            modalContent.innerHTML = `<p><strong>No data available for this day.</strong></p>`;
                        }

                        // Show the modal
                        modal.style.display = "flex";
                    })
                    .catch(error => console.error("Error fetching day details:", error));
            }
        });
    });

    // Close modal when clicking the close button or outside the modal
    modalClose.addEventListener("click", () => { modal.style.display = "none"; });
    window.addEventListener("click", (e) => { if (e.target === modal) modal.style.display = "none"; });
});
