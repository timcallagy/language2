$(document).ready(function(){

	//$("[id^=input-id]").click(function (){
	$("[class^=rating-container]").click(function (){
		rating_style = this.children[0].getAttribute("style");
		rating = (parseInt((rating_style.substring(7, rating_style.strlen)), 10)/20);
		practice_id = this.children[1].getAttribute("practice_id");
		var formData = new FormData();
		formData.append('rating', rating);
		var csrftoken = $.cookie('csrftoken');
		var xhr = new XMLHttpRequest();
		xhr.open('POST', '/practice/' +practice_id+ '/rating/', true);
		xhr.onload = function(e) {
			if (this.status == 200) {
				console.log(this.responseText);
			}
		};
		if(!this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
		xhr.send(formData);
	});
});
