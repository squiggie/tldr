$(document).ready( function () {

    // To ensure all AJAX calls have this in the header
    $.ajaxSetup({
        contentType: "application/json; charset=utf-8"
    });

    $("#submit").click(function() {
        // Grab string value from request text area
        var request = $("#request").val()  

        // Parse string to an object for clogs
        var requestObject = JSON.parse(request)

        //Print results
        console.log("Name: " + requestObject.name)

        // POST has the uri from app.py
        // POST needs request to be a string, or JSON.stringify of a JS object
        // Results is the JSON coming back
        $.post("/test", request).done(function(result) {

            // Result as an object
            console.log("Greeting: " + result.greeting)

            // Stringify result for pretty print reqpsonse
            var response = JSON.stringify(result);
            
            //display results
            $( "#response" ).text( response )

        })
    })
})