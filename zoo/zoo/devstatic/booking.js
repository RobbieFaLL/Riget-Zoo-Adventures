document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('event-calendar');

    if (!calendarEl) {
        console.error("Calendar element not found!");
        return;
    }

    var openingHoursUrl = calendarEl.getAttribute('data-opening-hours-url');
    var eventsUrl = calendarEl.getAttribute('data-events-url');

    if (!openingHoursUrl || !eventsUrl) {
        console.error("Missing opening hours or events URL");
        return;
    }

    console.log("Fetching data from:", openingHoursUrl, eventsUrl);

    fetch(openingHoursUrl)
        .then(response => response.json())
        .then(businessHoursData => {
            console.log("Opening hours received:", businessHoursData);

            fetch(eventsUrl)
                .then(response => response.json())
                .then(eventsData => {
                    console.log("Events received:", eventsData);

                    var calendar = new FullCalendar.Calendar(calendarEl, {
                        initialView: 'dayGridMonth',
                        headerToolbar: {
                            left: 'prev,next today',
                            center: 'title',
                            right: 'dayGridMonth,dayGridWeek,dayGridDay'
                        },
                        events: eventsData,  // Load events dynamically
                        businessHours: businessHoursData, // Load business hours dynamically
                        editable: false,
                        droppable: false,
                        eventBackgroundColor: '#378006', // Event background color
                        dayCellContent: function (arg) {
                            return arg.date.getDate(); // Ensure dates are correctly displayed
                        }
                    });

                    calendar.render();
                    console.log("Calendar successfully rendered!");
                })
                .catch(error => console.error("Error fetching events:", error));
        })
        .catch(error => console.error("Error fetching opening hours:", error));
});
