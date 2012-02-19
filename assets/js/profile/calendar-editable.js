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
            selectable: true,
            selectHelper: true,
            select: function(start, end, allDay) {
               var title = prompt('Event Title:');
               
               if(!title){
                  oops.notif('标题不能为空！');
                  return;
               }
               
               var startDate = $.fullCalendar.formatDate(start, 'yyyy-MM-dd HH:mm:ss');
               var endDate = $.fullCalendar.formatDate(end, 'yyyy-MM-dd HH:mm:ss');
               console.info('start: ' + startDate + ' end: ' + endDate);
               
               $.ajax({
                   url: '/schedule/crud',
                   type: 'PUT',
                   dataType: 'json',
                   data: $.toJSON({
                     starttime: startDate,
                     endtime: endDate,
                     content: title
                   }),
                   success: function(data){
                        console.info(data);
                        calendar.fullCalendar('renderEvent',
                        {
                            title: title,
                            start: start,
                            end: end,
                            allDay: allDay
                        },
                        true // make the event "stick"
                        );
                       oops.notif('成功增加日程');
                   },
                   error: function(){
                       oops.oops('增加日程失败');
                   }
               });
               calendar.fullCalendar('unselect');
            },
            editable: true,
            events: schedules
         });
      });
   });
});