$(document).ready(function() {

	$("[id^=likes]").click(function(){
	    var topicid;
	    topicid = $(this).attr("data-topicid");
	    $.get('/like_topic/', {topic_id: topicid}, function(data){
	    	$('#like_count'+topicid).html(data);
		$('#likes'+topicid).hide();
	    });
	});
});
