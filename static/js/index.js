$(document).ready(function(){
	var category_containers = $('.category_container');	
	var nav_links = $('.site_modify_link');

	//When a navbar link is clicked hide all other stream containers
	nav_links.click(function(event) {
		event.preventDefault();
		var toHide = $(this).attr('data-target');

		//If any actual fighting game names are clicked hide all others else show them all
		if (toHide != "All") {
			$(category_containers).each(function(){
				if ( $(this).attr('data-id') != toHide) {
					$(this).hide();
				}
				else {
					$(this).show();
				}
			});
		}
		else {
			$(category_containers).each(function(){
				$(this).show();
			});
		}
	});


});