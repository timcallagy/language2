$(document).ready(function() {

	
	$("[id^=finish-conference]").hide();

	var connection = new RTCMultiConnection();
	connection.session = {
		audio: true
	};

	connection.onstream = function(e) {
		audioContainer.insertBefore(e.mediaElement, audioContainer.firstChild);
	};

	
	if (!location.href.contains('coach')) {
	var sessions = {};
	connection.onNewSession = function(session) {
		console.log('stream - In Connection.onNewSession of language2_audio.');
		if (sessions[session.sessionid]) return;
		sessions[session.sessionid] = session;

		var tr = document.createElement('tr');
		tr.innerHTML = '<td id="session-started-msg">The Session has already started. <button class="join btn btn-primary">Join</button></td>';

		$("[id^=setup-new-conference]").hide();
		roomsList.insertBefore(tr, roomsList.firstChild);

		var joinRoomButton = tr.querySelector('.join');
		joinRoomButton.setAttribute('data-sessionid', session.sessionid);
		joinRoomButton.onclick = function() {
			$("[id^=finish-conference]").show();
			$("[id^=session-started-msg]").hide();
			var sessionid = this.getAttribute('data-sessionid');
			session = sessions[sessionid];
			if (!session) throw 'No such session exists.';
			console.log('Session to join: ' + session);
			connection.join(session);
		};
	};
	};

	var audioContainer = document.getElementById('audios-container') || document.body;
	var roomsList = document.getElementById('rooms-list');

	$("[id^=setup-new-conference]").click(function(){
		connection.open();
		$("[id^=setup-new-conference]").hide();
		$("[id^=finish-conference]").show();
	});

	$("[id^=finish-conference]").click(function(){
		$("[id^=finish-conference]").hide();
		$("[id^=setup-new-conference]").show();
		connection.close();
	});

	connection.connect();
});
