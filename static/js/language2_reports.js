//$(document).ready(function() {
$(window).load(function() {


	var audioElement = document.getElementById('main-audio');
	var audioStream;
        var recorder;
	var audioConstraints = {
	        audio: true,
	        video: false
	};


	$("[id^=play-error]").click(function(){
		console.log('In play-error');
		var min = parseInt(this.getAttribute("errorTimeMin"));
		var sec = parseInt(this.getAttribute("errorTimeSec"));
		audioElement.pause();
	//	audioElement.currentTime = 40; 
		audioElement.currentTime = (min*60) + sec - 4;
		console.log(audioElement.currentTime);
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
				var td_orig = document.createElement('td');
				td_orig.innerHTML = original_text;
				tr.appendChild(td_orig);
				var td_corr = document.createElement('td');
				td_corr.innerHTML = correction_text;
				tr.appendChild(td_corr);
				var delete_btn = document.createElement('button');
				delete_btn.innerHTML = "Delete Correction";
				delete_btn.id = "delete-writing-correction" + this.responseText;
				delete_btn.setAttribute("class", "btn btn-primary")
				delete_btn.setAttribute("pk", this.responseText)
				delete_btn.onclick = function() {
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
					if(!this.crossDomain){
						xhr.setRequestHeader("X-CSRFToken", csrftoken);
					}
					xhr.send(formData);
				};
				tr.appendChild(delete_btn);
		//		tr.innerHTML = '<td>' +original_text+ '</td><td>' +correction_text+ '</td><td><button class="btn btn-primary" id="delete-writing-correction' +this.responseText+ '" pk="' +this.responseText+ '">Delete Correction</td>';
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

});
