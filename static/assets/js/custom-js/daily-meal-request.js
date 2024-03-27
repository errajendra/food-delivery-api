$(document).ready(function() {
    $('#example1').DataTable();
} );


$(document).ready(function(){
    var firstName = $('#firstName').text();
    var intials = firstName.charAt(0).toUpperCase();
    var profileImage = $('#profileImage').text(intials);
  });


  
$(document).ready(function() {
    $(".show-hide-btn").click(function() {
      var id = $(this).data("id");
      $("#half-" + id).toggle();//hide/show..
      $("#full-" + id).toggle();
    });
  });
  
$(document).ready(function() {
    $(".hide-show-btn").click(function() {
      var id = $(this).data("id");
      $("#full-" + id).toggle();//hide/show..
      $("#half-" + id).toggle();
    });
  });


  $(document).ready(function() {
    $('#example1').DataTable();

    

    $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
      // Get the value entered in the filter input field (assuming you have an input field with ID "nameFilter")
      var filterValue = $('#searchUser').val().trim().toLowerCase();
      
      // Get the value in the "Name" column for the current row
      var nameColumnValue = data[3].toLowerCase();

      // Perform the filtering based on your criteria (e.g., simple substring matching)
      if (nameColumnValue.includes(filterValue)) {
        return true; // Display the row in the table
      }

      return false; // Hide the row from the table
    });

    // Trigger the custom filter when the user types in the filter input field
    $('#searchUser').on('keyup', function() {
      $('#example1').DataTable().draw(); // Redraw the table to apply the filter
    });



    $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
      // Get the value entered in the filter input field (assuming you have an input field with ID "nameFilter")
      var filterValue = $('#searchPlan').val().trim().toLowerCase();
      
      // Get the value in the "Name" column for the current row
      var nameColumnValue = data[4].toLowerCase();

      // Perform the filtering based on your criteria (e.g., simple substring matching)
      if (nameColumnValue.includes(filterValue)) {
        return true; // Display the row in the table
      }

      return false; // Hide the row from the table
    });

    // Trigger the custom filter when the user types in the filter input field
    $('#searchPlan').on('change', function() {
      $('#example1').DataTable().draw(); // Redraw the table to apply the filter
    });



    $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
      // Get the value entered in the filter input field (assuming you have an input field with ID "nameFilter")
      var filterValue = $('#searchType').val().trim().toLowerCase();
      
      // Get the value in the "Name" column for the current row
      var nameColumnValue = data[5].toLowerCase();

      // Perform the filtering based on your criteria (e.g., simple substring matching)
      if (nameColumnValue.includes(filterValue)) {
        return true; // Display the row in the table
      }

      return false; // Hide the row from the table
    });

    // Trigger the custom filter when the user types in the filter input field
    $('#searchType').on('change', function() {
      $('#example1').DataTable().draw(); // Redraw the table to apply the filter
    });



    $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
      // Get the value entered in the filter input field (assuming you have an input field with ID "nameFilter")
      var filterValue = $('#searchStatus').val().trim().toLowerCase();
      
      // Get the value in the "Name" column for the current row
      var nameColumnValue = data[7].toLowerCase();

      // Perform the filtering based on your criteria (e.g., simple substring matching)
      if (nameColumnValue.includes(filterValue)) {
        return true; // Display the row in the table
      }

      return false; // Hide the row from the table
    });

    // Trigger the custom filter when the user types in the filter input field
    $('#searchStatus').on('change', function() {
      $('#example1').DataTable().draw(); // Redraw the table to apply the filter
    });

} );
