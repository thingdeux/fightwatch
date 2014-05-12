$(document).ready(function(){
	var category_containers = $('.category_container');

	//When a navbar link is clicked hide all other stream containers
	$('.site_modify_link').click(function(event) {
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