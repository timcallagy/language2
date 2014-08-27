$(document).ready(function() {

	function countdownComplete(result){
               $("[id^=prepare-{{ practice.id }}]").hide();
               $("[id^=start-{{ practice.id }}]").show();
               alert('Hi');
        }
        var myCountdown1 = new Countdown({
               time:{{ practice.timeUntil }},
               hideLine : true,                
               rangeHi : "day",
               numbers : {
	               bkgd : "#FF9966"
               },
               onComplete : countdownComplete
        });


	

});
