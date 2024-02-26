// User-related functions
function checkoutDevice(deviceID) {
  // Send a POST request to /delete_device in views.py
  fetch("/checkout_device", {
    method: "POST",
    body: JSON.stringify({ deviceID: deviceID }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Reload the same page the user is currently on if successful
        window.location.href = window.location.href;
      } else {
        // Show an alert message with the error message
        alert(data.message);
      }
    });
}
// Function for logging in with a QR code
function login_w_qr_code(userId) {
  // Retrieve data from the modal form
  const scan_data = document.getElementById(`scan_data`).value;

  // Create a FormData object to send as form data
  const formData = new FormData();
  formData.append("userId", userId);
  formData.append("scan_data", scan_data);

  // Send a POST request to 'login' endpoint in auth.py
  fetch("/login", {
    method: "POST",
    body: formData,
  }).then((_res) => {
    // Redirect to the home page after successful login
    window.location.href = "/";
  });
}
// Function for assigning a device with a QR code
function assign_device_w_qr_code(userId) {
  // Retrieve data from the modal form
  const scan_data = document.getElementById(`scan_data`).value;

  // Create a FormData object to send as form data
  const formData = new FormData();
  formData.append("userId", userId);
  formData.append("scan_data", scan_data);

  // Send a POST request to the 'assign_device_w_qr_code' endpoint in views.py
  fetch("/assign_device_w_qr_code", {
    method: "POST",
    body: formData,
  })
    // Redirect to the home page after successful assignment
    .then((_res) => {
      window.location.href = "/";
    });
}
// Function for returning a device
function returnDevice(deviceID) {
  // Send a POST request to the 'return_device' endpoint in views.py
  fetch("/return_device", {
    method: "POST",
    body: JSON.stringify({ deviceID: deviceID }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Reload the same page the user is currently on if successful
        window.location.href = window.location.pathname;
      } else {
        // Show an alert message with the error message
        alert(data.message);
      }
    });
}
// Function for updating a device project from the home page
function updateDeviceProject(deviceID) {
  // Retrieve data from the form located on the user checked out calibrated and noncalibrated device tables.
  const project = document.getElementById(`project_${deviceID}`).value;

  // Create a FormData object to send as form data
  const formData = new FormData();
  formData.append("deviceID", deviceID);
  formData.append("project", project);

  // Send a POST request to the 'update_device_project' endpoint in views.py
  fetch("/update_device_project", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Reload the same page the user is currently on if successful
        window.location.href = window.location.pathname;
      } else {
        // Show an alert message with the error message
        alert(data.message);
      }
    });
}
// Function for updating a device location from the home page
function updateDeviceLocation(deviceID) {
  // Retrieve data from the form located on the user checked out calibrated and noncalibrated device tables.
  const location = document.getElementById(`location_${deviceID}`).value;

  // Create a FormData object to send as form data
  const formData = new FormData();
  formData.append("deviceID", deviceID);
  formData.append("location", location);

  // Send a POST request to the 'update_device_location' endpoint in views.py
  fetch("/update_device_location", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Reload the same page the user is currently on if successful
        window.location.href = window.location.pathname;
      } else {
        // Show an alert message with the error message
        alert(data.message);
      }
    });
}
// Function for generating a qr code from the device page
function generateQRCode(deviceID) {
  // Send a POST request to the 'generate_qrcode' endpoint in views.py
  fetch("/generate_qrcode", {
    method: "POST",
    body: JSON.stringify({
      deviceID: deviceID,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    // Handle the response as a binary blob
    .then((response) => response.blob())
    .then((blob) => {
      // Create a URL for the binary blob
      const url = window.URL.createObjectURL(blob);

      // Create a hidden anchor element to trigger the download
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;

      // Specify the filename for the downloaded file
      a.download = "qrcode.png";

      // Append the anchor element to the document body
      document.body.appendChild(a);

      // Programmatically trigger a click event on the anchor to initiate the download
      a.click();

      // Revoke the URL to release the resources
      window.URL.revokeObjectURL(url);
    })
    // Handle any errors that occur during the fetch operation
    .catch((error) => console.error("Error fetching the QR code:", error));
}

// Admin-related functions
function deleteDevice(deviceID) {
  // Send a POST request to /delete_device in views.py
  fetch("/delete_device", {
    method: "POST",
    body: JSON.stringify({ deviceID: deviceID }),
  })
    // Reload the /devices window
    .then((_res) => {
      window.location.href = window.location.href;
    });
}
function editUser(userId) {
  // Retrieve data from the modal form
  const user_name = document.getElementById(`user_name_${userId}`).value;
  const project = document.getElementById(`project_${userId}`).value;
  const email = document.getElementById(`email_${userId}`).value;
  const team = document.getElementById(`team_${userId}`).value;
  const admin = document.getElementById(`admin_${userId}`).checked;

  // Create a data object to send to the backend
  const data = {
    userId: userId,
    user_name: user_name,
    project: project,
    email: email,
    team: team,
    admin: admin,
  };

  // Send a POST request to Python backend
  fetch("/editUser", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    // Reload the /users page
    .then((_res) => {
      window.location.href = "/users";
    });
}
function updateUserPassword(userId) {
  // Retrieve data from the modal form
  const newPassword = document.getElementById(`password1_${userId}`).value;
  const confirmPassword = document.getElementById(`password2_${userId}`).value;

  // Create a FormData object to send as form data
  const formData = new FormData();
  formData.append("userId", userId);
  formData.append("newPassword", newPassword);
  formData.append("confirmPassword", confirmPassword);

  // Send a POST request to the Python backend
  fetch("/update_password", {
    method: "POST",
    body: formData,
  })
    // Reload the /users window
    .then((_res) => {
      window.location.href = "/users";
    });
}
function assignDevice(userId) {
  // Retrieve data from the modal form
  const deviceCategory = document.getElementById(
    `device_category_${userId}`
  ).value;
  const serialNumber = document.getElementById(`serial_number_${userId}`).value;

  // Create a data object to send to the backend
  const data = {
    userId: userId,
    deviceCategory: deviceCategory,
    serialNumber: serialNumber,
  };

  // Send a POST request to Python backend
  fetch("/assign_device", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    // Reload the /users page
    .then((_res) => {
      window.location.href = "/users";
    });
}
function generateUserQRCode(userID) {
  // Send a POST request to /generate_user_qrcode in views.py
  fetch("/generate_user_qrcode", {
    method: "POST",
    body: JSON.stringify({
      userID: userID,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    // Handle the response as a binary blob
    .then((response) => response.blob())
    .then((blob) => {
      // Create a URL for the binary blob
      const url = window.URL.createObjectURL(blob);

      // Create a hidden anchor element to trigger the download
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;

      // Specify the filename for the downloaded file
      a.download = "qrcode.png";

      // Append the anchor element to the document body
      document.body.appendChild(a);

      // Programmatically trigger a click event on the anchor to initiate the download
      a.click();

      // Revoke the URL to release the resources
      window.URL.revokeObjectURL(url);
    })
    // Handle any errors that occur during the fetch operation
    .catch((error) => console.error("Error fetching the QR code:", error));
}
function deleteUser(userID) {
  // Send a POST request to /delete_user in views.py
  fetch("/delete_user", {
    method: "POST",
    body: JSON.stringify({ userID: userID }),
  })
    // Reload the /users window
    .then((_res) => {
      window.location.href = "/users";
    });
}

// Handle radio button on device page.
function handleRadioClick(isCalibrated) {
  if (isCalibrated.value == "True") {
    document.getElementById("calibrated_table_container").style.display =
      "block";
    document.getElementById("noncalibrated_table_container").style.display =
      "none";
  } else {
    document.getElementById("calibrated_table_container").style.display =
      "none";
    document.getElementById("noncalibrated_table_container").style.display =
      "block";
  }
}

// Log user out after 5 minutes of inactivity
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

// Function to update under each device's return button timer on user home page.
function updateTimer(deviceId, checkoutTime) {
  var timerElement = document.getElementById("timer_" + deviceId);

  function update() {
    var currentTime = new Date().getTime();
    var checkoutTimestamp = new Date(checkoutTime).getTime();
    var timeDiffInSeconds = Math.floor(
      (currentTime - checkoutTimestamp) / 1000
    );
    var days = Math.floor(timeDiffInSeconds / (24 * 60 * 60));
    var hours = Math.floor((timeDiffInSeconds % (24 * 60 * 60)) / (60 * 60));
    var minutes = Math.floor((timeDiffInSeconds % (60 * 60)) / 60);

    timerElement.textContent = days + "d " + hours + "h " + minutes + "m ";
  }

  // Initial update
  update();

  // Set an interval to update the timer every minute (60,000 milliseconds)
  setInterval(update, 60000);
}
