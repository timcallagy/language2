$(document).ready(function() {

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
	var errorList = document.getElementById('error-list');

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
				console.log(this.responseText);
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

	var audioElement = document.getElementById('main-audio');

	$("[id^=play-error]").click(function(){
		console.log('In play-error');
		var min = parseInt(this.getAttribute("errorTimeMin"));
		var sec = parseInt(this.getAttribute("errorTimeSec"));
		audioElement.pause();
		console.log('ErrorTime Min: ' + min);
		console.log('ErrorTime sec: ' + sec);
		audioElement.currentTime = (min*60) + sec - 4;
		audioElement.play();
	        setTimeout(function(){
	        	audioElement.pause();
		}, 10000);
	});

	$("[id^=add-written-correction]").click(function(event){
		event.preventDefault();
	        error_pk = this.getAttribute("pk");
		error_correction = this.parentNode.children[0].value;
		console.log("Error Correction: " + error_correction);
		var formData = new FormData();
		formData.append('error_correction', error_correction);
		var csrftoken = $.cookie('csrftoken');
		var xhr = new XMLHttpRequest();
		xhr.open('POST', '/report/' +error_pk+ '/report_add_speech_correction/', true);
		xhr.onload = function(e) {
			if (this.status == 200) {
				var p = document.getElementById("written-correction-"+error_pk);
				p.innerHTML = error_correction;
//				var old_button = '[id^=add-written-correction-' +error_pk+ ']';
//				var new_button = '[id^=replace-written-correction-' +error_pk+ ']';
//				$(old_button).hide();
//				$(new_button).show();
			}
		};
		if(!this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
		xhr.send(formData);
	});

	var audioStream;
        var recorder;
	var audioConstraints = {
	        audio: true,
	        video: false
	};

			
	$("[id^=record-correction]").click(function(){
		audio = this.parentNode.children[0];
		error_pk = this.getAttribute("pk");
	        navigator.getUserMedia(audioConstraints, function(stream) {
	        	if (window.IsChrome) stream = new window.MediaStream(stream.getAudioTracks());
    			audioStream = stream;
                	audio.src = URL.createObjectURL(audioStream);
                          audio.muted = true;
                          audio.play();
			   var csrftoken = $.cookie('csrftoken');
			   mediaRecorder = new MediaStreamRecorder(stream);
			   mediaRecorder.mimeType = 'audio/ogg';
			   mediaRecorder.ondataavailable = function (blob) {
		   		var xhr = new XMLHttpRequest();
			       	xhr.open('POST', '/report/' +error_pk+ '/recording_correction_upload/', true);
				xhr.onload = function(e) {
			             if (this.status == 200) {
					var p = document.getElementById("audio-correction-"+error_pk);
					p.innerHTML = "Recording Uploaded";
//					var old_button = '[id^=record-correction-' +error_pk+ ']';
//					var new_button = '[id^=replace-record-correction-' +error_pk+ ']';
//					$(old_button).hide();
//					$(new_button).show();
				     }
				};
		        	if(!this.crossDomain) {
				         xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			        xhr.send(blob);
			   };
			   mediaRecorder.start(6100); // This sets the length of the recording. 
			   setTimeout(function(){
				   mediaRecorder.stop();
				   audio.pause();
			   }, 6000); //This sets the length of the media stream opening for recording.
	              }, function() {
	              });
		window.isAudio = true;
        });
	
	$("[id^=add-writing-correction]").click(function(){
		var pk = document.getElementById('practice_pk').innerHTML;
		original_text = this.parentNode.children[0].value;
		correction_text = this.parentNode.children[1].value;
		var tr = document.createElement('tr');
	        var csrftoken = $.cookie('csrftoken');
		var xhr = new XMLHttpRequest();
		var formData = new FormData();
		formData.append('original_text', original_text);
		formData.append('correction_text ', correction_text );
	       	xhr.open('POST', '/report/' +pk+ '/report_add_writing_correction/', true);
		xhr.onload = function(e) {
	        	if (this.status == 200) {
				tr.setAttribute("id", "error"+this.responseText);
				tr.innerHTML = '<td>' +original_text+ '</td><td>' +correction_text+ '</td><td><button class="btn btn-primary" id="delete-writing-correction' +this.responseText+ '" pk="' +this.responseText+ '">Delete Correction</td>';
				errorList.insertBefore(tr, errorList.rows.length.nextSibling);
                	}
		};
	       	if(!this.crossDomain) {
		         xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	        xhr.send(formData);

	});


	$("[id^=delete-writing-correction]").click(function(){
	        var csrftoken = $.cookie('csrftoken');
		var xhr = new XMLHttpRequest();
		var formData = new FormData();
		error_pk = this.getAttribute('pk');
		formData.append('error_pk', error_pk);
	       	xhr.open('POST', '/report/report_delete_writing_correction/', true);
		xhr.onload = function(e) {
	        	if (this.status == 200) {
				document.getElementById('error'+error_pk).style.display = "none";
                	}
		};
	       	if(!this.crossDomain) {
		         xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	        xhr.send(formData);
	});

	connection.connect();
});
