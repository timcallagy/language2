$(document).ready(function() {

	var audioElementCor = document.getElementById('correction');
	if (audioElementCor.getAttribute("isAudio") == "True"){
		$("[id^=no-audio-correction]").hide();
		$("[id^=play-correction]").show();

	} else {
		$("[id^=no-audio-correction]").show();
		$("[id^=play-correction]").hide();
	}


	$("[id^=play-error]").click(function(){
		var min = parseInt(this.getAttribute("errorTimeMin"));
		var sec = parseInt(this.getAttribute("errorTimeSec"));
		var audioElement = document.getElementById('recording');
		var uniqueId = audioElement.getAttribute("uniqueId");
		audioElement.pause();
		audioElement.currentTime = (min*60) + sec - 4;
		audioElement.play();
	        setTimeout(function(){
			var audioElement = document.getElementById('recording');
			var currentId = audioElement.getAttribute("uniqueId");
			// Only pause the audio if the identifier of a specific audio clip hasn't changed.
			if (uniqueId == currentId) {
		        	audioElement.pause();
			}
		}, 10000);
	});
	
	$("[id^=show-correction]").click(function(){
		$("[id^=correction-cover]").hide();
		var audioElement = document.getElementById('correction');
		if (audioElement.getAttribute("isAudio") == "False") {
			$("[id^=play-correction]").hide();
			$("[id^=no-audio-correction]").show();
		} else {
			$("[id^=no-audio-correction]").hide();
			$("[id^=play-correction]").show();
		}
		var writtenElement = document.getElementById('written-correction')
		if (!writtenElement.innerHTML){
			$("[id^=written-correction]").hide();
			$("[id^=no-written-correction]").show();
		} else {
			$("[id^=no-written-correction]").hide();
			$("[id^=written-correction]").show();
		}
		$("[id^=correction-objects]").show();

	});

	$("[id^=play-correction]").click(function(){
		var audioElement = document.getElementById('correction');
		audioElement.play();
	});
			

	$("[id^=next-error]").click(function(){
		$.get("/practice/next_error/", function(data){

			$("#mistakes-panel").fadeOut(100);
			$("[id^=correction-objects]").hide();
			$("[id^=correction-cover]").fadeOut(100);
			$("[id^=correction-cover]").fadeIn(1000);
		

			// "Recording" audio element set up.
			var audioElementRec = document.getElementById('recording');
			var src = audioElementRec.getAttribute('src');
			var tokens = src.split('/');
			var S3 = tokens[0] + '/' + tokens[1] + '/' + tokens[2] + '/'; 
			audioElementRec.setAttribute("src", S3 + data[1].fields.recording);
			// Set a unique identifier between 0 and 1000 on this specific audio clip.
			var randomnumber=Math.floor(Math.random()*1001);
			audioElementRec.setAttribute("uniqueId", randomnumber);

			// "PlayError" button set up.
			var btn = document.getElementById('play-error');
			btn.setAttribute("errorTimeMin", data[0].fields.error_time_min);
			btn.setAttribute("errorTimeSec", data[0].fields.error_time_sec);

			// "Correction" audio element set up.
			var audioElementRec = document.getElementById('correction');
			if (data[0].fields.correction_recording_flag == true){
				var src = audioElementRec.getAttribute('src');
				var tokens = src.split('/');
				var S3 = tokens[0] + '/' + tokens[1] + '/' + tokens[2] + '/'; 
				audioElementRec.setAttribute("src", S3 + data[0].fields.correction_recording);
				audioElementRec.setAttribute("isAudio", "True"); 
			} else {
				audioElementRec.setAttribute("isAudio", "False"); 
			}

			// "WrittenCorrection" element set up.
			var elem = document.getElementById('written-correction');
			if (data[0].fields.correction_text){
				elem.innerHTML = data[0].fields.correction_text;
			} else {
				elem.innerHTML = "";
			}


			$("#mistakes-panel").fadeIn(1000);
		
			// Auto-play the next mistake.	
	        	setTimeout(function(){
	        		btn.click();
			}, 1000);
		});
	});

});
