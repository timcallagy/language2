$(function(){
  $.datepicker.setDefaults(
    $.extend( $.datepicker.regional[ '' ] )
  );
  $( '#id_start_0' ).datepicker();
  $( '#id_end_0' ).datepicker();
  $( '#id_end_recurring_period' ).datepicker();
  $( '#id_start_1' ).timePicker({ timeFormat: 'H:i' });
  $( '#id_end_1' ).timePicker({ timeFormat: 'H:i' });

  $( '[id^=id_dateTime_0]' ).datepicker({dateFormat: 'yy-mm-dd'});
  $( '[id^=id_dateTime_1]' ).timePicker({ timeFormat: 'H:i' });
});
