// User-related functions

var reserveModal = document.getElementById('reserveDeviceModal');
reserveModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  var button = event.relatedTarget;
  // Extract the data-device-id attribute from the button
  var deviceId = button.getAttribute('data-device-id');

  // Use the value to set the hidden input's value in the modal
  var hiddenInput = reserveModal.querySelector('#hiddenDeviceId');

  hiddenInput.value = deviceId;
});

// Handle radio button on device page.
function handleRadioClick(isCalibrated) {
  if (isCalibrated.value == "True") {
    document.getElementById("calibrated_table_container").style.display =
      "block";
    document.getElementById("noncalibrated_table_container").style.display =
      "none";
      document.getElementById("reservations_table_container").style.display =
      "none";
  } else if (isCalibrated.value == "False") {
    document.getElementById("calibrated_table_container").style.display =
      "none";
    document.getElementById("noncalibrated_table_container").style.display =
      "initial";
      document.getElementById("reservations_table_container").style.display =
      "none";
  }
  else {
    document.getElementById("calibrated_table_container").style.display =
      "none";
    document.getElementById("noncalibrated_table_container").style.display =
      "none";
    document.getElementById("reservations_table_container").style.display =
      "block";
  }
}

// Log user out after 15 minutes of inactivity
let inactivityTimer;

function startInactivityTimer() {
  inactivityTimer = setTimeout(logoutAfterInactivity, 15 * 60 * 1000); // Set duration here
}
function resetInactivityTimer() {
  clearTimeout(inactivityTimer);
  startInactivityTimer();
}

function logoutAfterInactivity() {
  window.location.href = "/logout"; // Redirect to the logout route
}

// Add event listeners to reset the timer on user interaction
window.addEventListener("click", resetInactivityTimer);
window.addEventListener("keydown", resetInactivityTimer);

// Start the timer when the page loads
startInactivityTimer();