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
//			if ($("[id^=waiting-for-mic]").is(":visible") || $("[id^=connecting]").is(":visible") || $("[id^=in-progress]").is(":visible") || $("[id^=call-ended]").is(":visible")){  /// This line causes the Join button to be hidden if the coach leg drops and rejoins.
			if ($("[id^=waiting-for-mic]").is(":visible") || $("[id^=connecting]").is(":visible") || $("[id^=in-progress]").is(":visible")){  

//				$("[id^=coach-joined-msg]").hide();
				return;
			} else {
			sessions[session.sessionid] = session;
			$("[id^=waiting-for-coach]").hide();
			$("[id^=call-dropped]").hide();
			$("[id^=coach-joined-msg]").show();
			$("[id^=rooms-list]").show();
			var oldJoinRoomButton = document.getElementById("join-button");
			var joinRoomButton = document.createElement('input');
			joinRoomButton.setAttribute('type', 'button');
			joinRoomButton.setAttribute('id', 'join-button');
			joinRoomButton.setAttribute('class', 'btn btn-primary');
			joinRoomButton.setAttribute('value', 'Join');
			joinRoomButton.setAttribute('data-sessionid', session.sessionid);
			joinRoomButton.onclick = function() {
				console.info('%%% Join button clicked.');
				$("[id^=rooms-list]").hide();
				$("[id^=coach-joined-msg]").hide();
				$("[id^=waiting-for-mic]").show();
				var sessionid = this.getAttribute('data-sessionid');
				session = sessions[sessionid];
				if (!session) throw 'No such session exists.';
				console.info('Session to join: ');
				console.info(session);
				connection.join(session);
			};
			roomsList.insertBefore(joinRoomButton, oldJoinRoomButton);
			roomsList.removeChild(oldJoinRoomButton);
			}
		};
	};



	$("[id^=setup-new-conference]").click(function(){
		connection.open();
		$("[id^=setup-new-conference]").hide();
		$("[id^=session-started]").hide();
		$("[id^=waiting-for-mic]").show();
	});

	$("[id^=speaking-error]").click(function(){
		var pk = document.getElementById('practice_pk').innerHTML;
		var csrftoken = $.cookie('csrftoken');
		var xhr = new XMLHttpRequest();
		xhr.open('POST', '/practice/'+pk+'/speaking_error_notification/', true);
		xhr.onload = function(e) {
			if (this.status == 200) {
				console.info(this.responseText);
				var tr = document.createElement('tr');
				tr.innerHTML = '<td id="speaking-error" class="bg-info">&nbsp;&nbsp;&nbsp;' + this.responseText.substring(2, 7) + '</p></td>';
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
		$("[id^=in-progress]").hide();
		connection.close();
	});

	connection.connect();
});
