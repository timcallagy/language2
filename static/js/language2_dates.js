$(function(){
  $.datepicker.setDefaults(
    $.extend( $.datepicker.regional[ '' ] )
  );
  $( '#id_start_0' ).datepicker();
  $( '#id_end_0' ).datepicker();
  $( '#id_end_recurring_period' ).datepicker();
  $( '#id_start_1' ).timePicker({ timeFormat: 'H:i' });
  $( '#id_end_1' ).timePicker({ timeFormat: 'H:i' });

  $( '[id^=id_dateTime_0]' ).datepicker({
	  dateFormat: 'yy-mm-dd',
   	  onSelect: function(selectedDate) {
		$('#unavailability_msg').hide();	
  		$( '#checking_unavailability').show();
		var xhr = new XMLHttpRequest();
		year = selectedDate.substring(0, 4);
		month = selectedDate.substring(5, 7);
		day = selectedDate.substring(8, 10);
		xhr.open('GET', '/coach/unavailability/' + year + '/' + month + '/' + day + '/', true);
		xhr.onload = function(e) {
			if (this.status == 200) {
				list = JSON.parse(this.responseText);
				var listElement = document.getElementById('unavailability_list');
				listElement.innerHTML = "";
				for (var i = 0; i < list.length; i++){
					listElement.appendChild(document.createTextNode(list[i]));
					listElement.appendChild(document.createElement("br"));
				}
  				$( '#checking_unavailability').hide();
				$('#unavailability_msg').show();	
			}
		};
		xhr.send();
          // send date by xhr
          // display response under datepicker
  	}
  });

  $( '[id^=id_dateTime_1]' ).timePicker({ timeFormat: 'H:i', 'useselect': true, disableTimeRanges: [['02:00', '03:00'],['2pm', '3pm']] });
});
