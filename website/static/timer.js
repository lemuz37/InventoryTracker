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
  