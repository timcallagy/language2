$(document).ready(function() {

	$("[id^=likes]").click(function(){
	    var topicid;
	    topicid = $(this).attr("data-topicid");
	    $.get('/like_topic/', {topic_id: topicid}, function(data){
	    	$('#like_count'+topicid).html(data);
		$('#likes'+topicid).hide();
	    });
	});

	var connection = new RTCMultiConnection();
	connection.session = {
		audio: true
	};

	connection.onstream = function(e) {
		audioContainer.insertBefore(e.mediaElement, audioContainer.firstChild);
	};

	var sessions = {};
	connection.onNewSession = function(session) {
		if (sessions[session.sessionid]) return;
		sessions[session.sessionid] = session;

		var tr = document.createElement('tr');
		tr.innerHTML = '<td>The Session has already started. <button class="join btn btn-primary">Join</button></td>';

		$("[id^=setup-new-conference]").hide();
		roomsList.insertBefore(tr, roomsList.firstChild);

		var joinRoomButton = tr.querySelector('.join');
		joinRoomButton.setAttribute('data-sessionid', session.sessionid);
		joinRoomButton.onclick = function() {
			this.disabled = true;
			var sessionid = this.getAttribute('data-sessionid');
			session = sessions[sessionid];
			if (!session) throw 'No such session exists.';
			connection.join(session);
		};
	};

	var audioContainer = document.getElementById('audios-container') || document.body;
	var roomsList = document.getElementById('rooms-list');
	$("[id^=setup-new-conference]").click(function(){
		connection.open();
		$("[id^=setup-new-conference]").hide();
	});
	connection.connect();
});
