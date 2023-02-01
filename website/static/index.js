function returnDevice(deviceID) {
    fetch("/return-device", {
        method: "POST",
        body: JSON.stringify({ deviceID: deviceID}),
    }).then((_res) => {
        window.location.href = "/";
    });
}

function checkOutDevice(deviceID) {
    fetch("/check-out-device", {
        method: "POST",
        body: JSON.stringify({ deviceID: deviceID}),
    }).then((_res) => {
        window.location.href = "/";
    });
}
