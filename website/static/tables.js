// DataTable initialization

// Data table for user calibrated devices.
$(document).ready(function () {
  $("#home_calibrated").DataTable({
    scrollY: "50vh", // Vertical scrolling. Here, 'vh' stands for viewport height. You can also set it in pixels e.g., '300px'.
    scrollX: true, // Horizontal scrolling.
    scrollCollapse: true,
    paging: true, // Enable pagination
    lengthMenu: [5, 10, 15, 20, 25, 50, 100],
    pageLength: 5, // Number of rows per page
  });
});

// Data table for user non-calibrated devices.
$(document).ready(function () {
  $("#home_noncalibrated").DataTable({
    scrollY: "50vh", // Vertical scrolling. Here, 'vh' stands for viewport height. You can also set it in pixels e.g., '300px'.
    scrollX: true, // Horizontal scrolling.
    scrollCollapse: true,
    paging: true, // Enable pagination
    lengthMenu: [5, 10, 15, 20, 25, 50, 100],
    pageLength: 5, // Number of rows per page
    // Add more options as needed
  });
});

// Data table for calibrated devices page.
$(document).ready(function () {
  $("#calibrated_table").DataTable({
    paging: true,
    ordering: true,
    searching: true,
    lengthMenu: [5, 10, 25, 50, 100],
    pageLength: 5,
    responsive: true,
    dom: "flrtiBp", // Include buttons for CSV export
    buttons: [
      {
        extend: "csv", // Use the CSV export button
        text: "Export to CSV", // Customize the button text
        exportOptions: {
          columns: [1, 2, 3, 4, 5], // Specify the columns you want to export (e.g., columns 1, 2, and 3).
        },
      },
    ],
    columnDefs: [
      {
        targets: 0,
        width: "128.767px"
      }
    ],
    autoWidth: false
  });
});

// Data table for noncalibrated devices page.
$(document).ready(function () {
  $("#noncalibrated_table").DataTable({
    paging: true,
    ordering: true,
    searching: true,
    lengthMenu: [5, 10, 25, 50, 100],
    pageLength: 5,
    responsive: true,
    dom: "flrtiBp", // Include buttons for CSV export
    buttons: [
      {
        extend: "csv", // Use the CSV export button
        text: "Export to CSV", // Customize the button text
        exportOptions: {
          columns: [1, 2, 3], // Specify the columns you want to export (e.g., columns 1, 2, and 3).
        },
      },
    ],
    columnDefs: [
      {
        targets: 0,
        width: "128.767px"
      }
    ],
    autoWidth: false
  });
});

// Data table for reservations devices page.
$(document).ready(function () {
  $("#reservations_table").DataTable({
    paging: true,
    ordering: true,
    searching: true,
    lengthMenu: [5, 10, 25, 50, 100],
    pageLength: 5,
    responsive: true,
    columnDefs: [
      {
        targets: 0,
        width: "128.767px"
      }
    ],
    autoWidth: false
  });
});

// Data table for update devices page.
$(document).ready(function () {
  $("#update_device_table").DataTable({
    paging: true, // Enable pagination
    lengthMenu: [5, 10, 15, 20, 25, 50, 100],
    pageLength: 5, // Number of rows per page
  });
});

// Data table for user page.
$(document).ready(function () {
  $("#user_table").DataTable({
    paging: true, // Enable pagination
    pageLength: 5, // Number of rows per page
    lengthMenu: [5, 10, 15, 20, 25, 50, 100],
    // Add more options as needed
  });
});

// Event handling for modals and inactivity
// Focus on input field when scan device modal opens
$("#scanDeviceModal").on("shown.bs.modal", function () {
  $(this).find("#scan_data").focus().select();
});

// Focus on input field when scan device modal opens
$("#scanQRCodeModal").on("shown.bs.modal", function () {
  $(this).find("#scan_data_home").focus().select();
});
