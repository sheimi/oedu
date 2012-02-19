/**
 * Ajax script file for index page.
 * Suppose jQuery script file is included.
 * author: kavinyao
 * revision: 9
 */

$(document).ready(function(){
   oops.notif('正在努力地加载状态...', 2000);
   
   $.ajax({
    url: "/status/statuslist/all",
    dataType: "json",
    success: function(data){
      $('a#show-status').addClass('loaded');
      var newsList = $('#news-list');
      $.each(data, function(i, status){
          var newItem = $(oops.makeStatusLi(status));
          newItem.hide();
          newItem.appendTo(newsList).slideDown('slow');
      });
      set_share_dialog();
    }
   });
   
   $.ajax({
    url: "/anno/annolist",
    dataType: "json",
    success: function(data){
      if(!data.length){
         //no annoucements
         //does not display
         return;
      }
      var annoList = $('#announcements-list');
      $.each(data, function(i, anno){
          var newAnno = $(oops.makeAnnoLi(anno));
          newAnno.appendTo(annoList);
      });
      
      $('#announcements-area').slideDown();
      set_share_dialog();
    }
   });
   
   $('#show-status').click(function(e){
      e.preventDefault();
      
      $('#share-area').hide();
      $('#news-area').show();
   });
   
   $('#show-share').click(function(e){
      e.preventDefault();
      
      $('#news-area').hide();
      $('#share-area').show();
      
      if($(this).hasClass('loaded')){
         //already loaded
         return;
      }
      
      $(this).addClass('loaded');
      $.getJSON('/share/share_list/user/', null, function(data){
         var shareList = $('#share-list');
         $.each(data, function(index, share){
            var shareLi = $(oops.makeShareLi(share));
            shareLi.hide().appendTo(shareList).slideDown();
            set_share_dialog();
         });
      });
   });
   
   $('#fdy-special').click(function(e){
      e.preventDefault();
      
      $.fancybox.showActivity();
      $('#news-list li').slideUp();
      $('#share-list li').slideUp();
      
      var url = null;
      var url2 = null;
      if($(this).hasClass('all')){
         $(this).removeClass('all').html('查看所有更新');
         url = '/status/statuslist/special';
         url2 = '/share/sharelist/special';
      }else{
         $(this).addClass('all').html('只看团学组织');
         url = '/status/statuslist/all';
         url2 = '/share/share_list/all';
      }
      
      setTimeout(function(){
         $('#news-list li').remove();
         $('#share-list li').remove();
         
         $.getJSON(url, {}, function(data){
            var newsList = $('#news-list');
            $.each(data, function(i, status){
               var newItem = $(oops.makeStatusLi(status));
               newItem.hide();
               newItem.appendTo(newsList).slideDown('slow');
               $.fancybox.hideActivity();
            });
            set_share_dialog();
         });
         
         $.getJSON(url2, {}, function(data){
            var shareList = $('#share-list');
            $.each(data, function(i, share){
               var newItem = $(oops.makeShareLi(status));
               newItem.hide();
               newItem.appendTo(shareList).slideDown('slow');
               $.fancybox.hideActivity();
            });
            set_share_dialog();
         });
      }, 2000);
   });
   
   $('#status-input').focusin(function(){
      $(this).animate({height: '90px'}, 500);
   }).focusout(function(){
      $(this).animate({height: '60px'}, 500);
   });
   
   $('#status-input').keydown(function(event){
      if(event.which == 13){
         event.preventDefault();
         
         $('#status-submit').trigger('click');
      }
   });
   
   $('#status-submit').click(function(event){
      event.preventDefault();
      
      var status = $('#status-input').val();
      if(!status){
         oops.notif('状态内容太不能为空！');
         return;
      }
      
      if(status.length > 140){
         oops.notif('状态得在140字内哦，亲~');
         return;
      }
      
      $.ajax({
         url: '/status/crud',
         type: 'PUT',
         data: $.toJSON({content: status}),
         dataType: 'json',
         success: function(id){
            oops.notif('更新状态成功！');
            $('#status-input').val('').trigger('focusout');
            $.ajax({
               url: '/status/crud/' + id,
               type: 'GET',
               dataType: 'json',
               success: function(data){
                  var statusLi = $(oops.makeStatusLi(data[0]));
                  statusLi.hide();
                  $('#news-list').prepend(statusLi);
                  statusLi.slideDown('slow');
                  set_share_dialog();
               },
               error: function(){
                  oops.notif('Oops，获取最新状态失败:(');
               }
            });
         },
         error: function(){
            oops.notif('Oops，更新状态失败:(')
         }
      });
   });
   
   function set_share_dialog(){
       $('a.status-share').fancybox({
            transitionIn: 'elastic',
            transitionOut: 'elastic',
            overlayOpacity: 0.1,
            opacity: true
       });
   }
});