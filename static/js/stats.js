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

    function getRecord(names) {
        $.ajax({
            type: "GET",
            url: "/stats/fighter/generate",
            data: {
                'q': names
            },
            cache: false
        })
        .success(function (result) {
            // Get the fighter stats from elasticsearch
            var stats = JSON.parse(result)
            ele = $("#stats")            
            ele.html("<table>\
                    <tr>\
                        <th>WINS</th>\
                        <th>LOSSES</th>\
                    </tr>\
                    <tr>\
                        <td>" + stats['wins'] + "</td>\
                        <td>" + stats['losses'] + "</td>\
                    </tr>\
                </table>");
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
                // Build query paramter to pass to /fighter
                final_query = ""                
                for (x=0; x < checked.length;x++) {
                    if (x == checked.length - 1) { 
                        final_query += checked[x].value
                    }
                    else {
                        final_query += checked[x].value + ",";
                    }
                }
                getRecord(final_query);
            }
        }
    });

    
});


