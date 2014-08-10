$(document).ready(function() {


	var audioContainer = document.getElementById('audios-container') || document.body;
	var roomsList = document.getElementById('rooms-list');
	var errorList = document.getElementById('error-list');
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
			console.info('%%% In Connection.onNewSession of language2_audio.');
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
				console.info('Session to join: ');
				console.info(session);
				connection.join(session);
			};
		};
	};


	$("[id^=setup-new-conference]").click(function(){
		connection.open();
		$("[id^=setup-new-conference]").hide();
		$("[id^=finish-conference]").show();
		$("[id^=speaking-error]").show();
	});

	$("[id^=speaking-error]").click(function(){
		var pk = document.getElementById('practice_pk').innerHTML;
		var csrftoken = $.cookie('csrftoken');
		var xhr = new XMLHttpRequest();
		xhr.open('POST', '/practice/speaking_error_notification/'+pk+'/', true);
		xhr.onload = function(e) {
			if (this.status == 200) {
				console.info(this.responseText);
				var tr = document.createElement('tr');
				tr.innerHTML = '<td id="speaking-error">Speaking Error at: ' + this.responseText.substring(3, 7) + '</td>';
				errorList.insertBefore(tr, errorList.firstChild);
			}
		};
		if(!this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
		xhr.send();
	});


	$("[id^=finish-conference]").click(function(){
		$("[id^=finish-conference]").hide();
		$("[id^=create-report]").show();
		$("[id^=speaking-error]").hide();
		connection.close();
	});

	connection.connect();
});
