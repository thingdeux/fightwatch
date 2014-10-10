$(document).ready(function() {
    function queryName(name_to_query, tracker, location) {
        // Query fighter route and return a list of names
        $.ajax({
            type: "GET",
            url: "/stats/fighter",
            data: {
                'name': name_to_query
            },
            cache: false           
        })
        .success(function (result) {
            var results = JSON.parse(result)['names'];
            //$(tracker).append()
            
            /* Append table rows to the alias section to allow for
               selecting multiple aliases for a fighter */                       
            for (x=0; x < results.length; x++) {                
                $(location).append(
                    '<tr><td><input type="checkbox" value="' + results[x] + '""></input></td>\
                    <td class="alias">' + results[x] + '</td></tr>'
                );
            }            
        });        
    }

    // Handler for name search box (populates alias list)
    $(".name_searcher").on('submit click', function(event)  {        
        event.preventDefault();
        tar = $(event.target)

        if (event.type == "submit") {
            // Get the name query from the input field on enter
            query = $(this).find('.form-control').val()                        
            queryName(query,"#queried", "#results");            
        }
        else if ((event.type == "click") && (event.target.nodeName == "BUTTON")) {
            // If the search button is clicked, also query a name
            if (tar.hasClass('search_it')) {
                query = $(this).find('.form-control').val()                        
                queryName(query,"#queried", "#results");  
            }
            else if (tar.hasClass('generate_it')) {
                // Handler for generate button
                checked = $('input:checked');
                for (x=0; x < checked.length;x++) {
                    console.log(checked[x].value);
                }
            }
        }
    });

    
});


