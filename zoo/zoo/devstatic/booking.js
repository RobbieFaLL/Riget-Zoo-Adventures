document.addEventListener("DOMContentLoaded", function () {
    // Highlight today's date in the calendar
    highlightToday();

    // Add event listeners for calendar navigation
    const prevMonthBtn = document.getElementById("prev-month");
    const nextMonthBtn = document.getElementById("next-month");

    if (prevMonthBtn && nextMonthBtn) {
        prevMonthBtn.addEventListener("click", function () {
            navigateMonth(-1);
        });
        nextMonthBtn.addEventListener("click", function () {
            navigateMonth(1);
        });
    }

    // Booking form validation
    const bookingForm = document.querySelector("form");
    if (bookingForm) {
        bookingForm.addEventListener("submit", function (event) {
            if (!validateForm()) {
                event.preventDefault();
            }
        });
    }
});

// Function to navigate calendar months
function navigateMonth(offset) {
    const currentMonth = parseInt(document.getElementById("calendar").dataset.month);
    const currentYear = parseInt(document.getElementById("calendar").dataset.year);

    let newMonth = currentMonth + offset;
    let newYear = currentYear;

    if (newMonth < 1) {
        newMonth = 12;
        newYear--;
    } else if (newMonth > 12) {
        newMonth = 1;
        newYear++;
    }

    window.location.href = `/calendar/${newYear}/${newMonth}/`;
}

// Function to validate booking form
function validateForm() {
    let isValid = true;
    let requiredFields = document.querySelectorAll("form input[required], form textarea[required]");

    requiredFields.forEach((field) => {
        if (!field.value.trim()) {
            field.classList.add("error");
            isValid = false;
        } else {
            field.classList.remove("error");
        }
    });

    return isValid;
}

// Function to highlight today's date in the calendar
function highlightToday() {
    const today = new Date();
    const todayDate = today.getDate();
    const currentMonth = today.getMonth() + 1;
    const currentYear = today.getFullYear();

    document.querySelectorAll(".calendar td").forEach((cell) => {
        if (
            parseInt(cell.dataset.day) === todayDate &&
            parseInt(cell.dataset.month) === currentMonth &&
            parseInt(cell.dataset.year) === currentYear
        ) {
            cell.classList.add("today");
        }
    });
}
