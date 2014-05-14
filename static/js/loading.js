$(document).ready(function(){

	function checkDBUp() {
		//If DB up, reload - else set a new timeout for 2 seconds
		$.get("/checkDB", function (data, status) {
			if (status == "success") {
				if (data == "True") {					
					setTimeout(function(){ checkDBUp() } , 3000);
				}
				else {
					location.reload();
				}

			}
			
		});

		//setTimeout(function()) { checkDBUp(), 3000	}		
	}

	setTimeout(function(){ checkDBUp() } , 3000);

});