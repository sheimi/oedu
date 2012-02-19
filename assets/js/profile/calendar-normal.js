$(document).ready(function(){
    var uid = oops.getUserIdFromPath();
    
    $('#menu li.agenda').click(function(e){
      var agenda = $('#agenda');
      if(agenda.hasClass('rendered')){
         //calendar already rendered
         return;
      }
      
      agenda.addClass('rendered');
      
      $.getJSON('/schedule/schedule_list/'+uid, null, function(schedules){
         var calendar = $('#agenda').fullCalendar({
            header: {
               left: 'prev,next today',
               center: 'title',
               right: 'month,agendaWeek,agendaDay'
            },
            events: schedules
         });
      });
   });
});