function returnDevice(deviceID) {
    fetch("/return_device", {
        method: "POST",
        body: JSON.stringify({ deviceID: deviceID}),
    }).then((_res) => {
        window.location.href = "/";
    });
}

function checkOutDevice(deviceID) {
    fetch("/check_out_device", {
        method: "POST",
        body: JSON.stringify({ deviceID: deviceID}),
    }).then((_res) => {
        window.location.href = "/devices";
    });
}