/**
 * Ajax script file for profile page.
 * author: kavinyao
 * revision: 17
 * dependency: oops-global.js
 */

$(document).ready(function(){
   var uid = oops.getUserIdFromPath();
   
   $('#agenda-form-cancal').click(function(){
      //empty fields!
      $('#agenda-add-form').slideUp();
   });
   
   $('a#profile-start-chat').click(function(event){
      event.preventDefault();
      console.info('get raw id: ' + uid);
      
      if(!uid){
         //it's the current user
         return;
      }
      
      var username = '';
      $.ajax({
         url: '/core/crud/'+uid,
         async: false, //IMPORTANT!
         success: function(user){
            username = user[0].name;
         }
      });
      
      oops.im.construct_window_if_not_exist(parseInt(uid), username);
   });
   
   $('a#profile-add-tag').click(function(event){
      event.preventDefault();
      
      var addTagInput = $('<input id="oops-add-tag-temp" size="5" style="border-radius: 3px;border-style:solid; margin-right: 5px;" />');
      addTagInput.keydown(function(event){
         if(event.which !== 13){
            //not interested
            return;
         }
         event.preventDefault();
         var newTag = $(this).val();
         if(!newTag){
            oops.notif("Cannot add an empty tag!");
            return;
         }
         
         
         var isExists = false;
         $('#tag-list li.tag-item a').each(function(i){
            if(newTag === $(this).html()){
               isExists = true;
            }
         });
         
         if(isExists){
            oops.oops('此tag已经存在！');
            return;
         }
         
         $.ajax({
            url: '/core/tag/crud/',
            type: 'PUT',
            data: $.toJSON({description: newTag}),
            dataType: 'json',
            success: function(id){
               //get the tag displayed
               var tagLi = $('<li class="tag-item"><a href="/search?query=' + newTag + '&tag">' + newTag + '</a></li>');
               $('li#tag-add').before(tagLi);
               
               //associate the tag with current user
               var user_id = oops.getUserIdFromPath();
               var users = [];//TODO get default user's id
               if(user_id){
                  users.push(parseInt(user_id));
               }
               //console.info(users);
               
               $.ajax({
                  url: '/core/tag/crud/' + id,
                  type: 'POST',
                  data: $.toJSON({
                     operation: 'add',
                     users: users
                  }),
                  dataType: 'json',
                  success: function(data){
                     oops.notif('关联tag成功');
                  }
               });
            },
            error: function(data){
               console.err(data);
            }
         });
         
         $(this).remove();
      }).focusout(function(){
         $(this).remove();
      });
      
      $(this).before(addTagInput);
      addTagInput.focus();
   });
   
   $('#message-submit').click(function(e){
      e.preventDefault();
      
      var message = $('#message-input').val();
      $.ajax({
         url: '/message/crud',
         type: 'PUT',
         dataType: 'json',
         data: $.toJSON({
            message: message,
            to_user: uid
         }),
         success: function(id){
            oops.notif('留言成功！');
            $('#message-input').val('');
            $.getJSON('/message/crud/'+id, null, function(data){
               var message = data[0];
               var from_user = oops.tryGetProfileFromCache(message.fields.from_user);
               var messageLi = $('<li><div class="img"><img class="avatar" src="/static/images/profile/' + message.fields.from_user + '"  width="40" height="40" alt="no pic"></div><div class="content"><a href="/core/profile/' + message.fields.from_user + '">' + from_user.name + '</a> 留言说：' + message.fields.message +'</div><p class="clear"></p></li>');
               messageLi.hide().prependTo($('#leave-messages-list')).slideDown();
            });
         },
         error: function(){
            oops.oops('留言失败！');
         }
      });
   });
   
   function makeTagLi(tag){
      return '<li class="tag-item"><a href="/search/tag/' + tag.fields.description + '">' + tag.fields.description + '</a></li>';
   }
   
   $('.feedback-area span.title').toggle(function(){
      $('.detail', $(this).parent()).slideDown();
   }, function(){
      $('.detail', $(this).parent()).slideUp();
   });
   
   $('.feedback-area input.feedback-reply-button').live('click', function(){
      var reply = $(this).prev().val();
      var fid = $(this).next().html();
      
      //TODO
   });
   
   $('.profile-question-area span.title').toggle(function(){
      $('.detail', $(this).parent()).slideDown();
   }, function(){
      $('.detail', $(this).parent()).slideUp();
   });
   
   $('.profile-question-area input.question-reply-button').live('click', function(){
      var answer_input = $(this).prev();
      var reply = answer_input.val();
      var qid = $(this).next().html();
      
      if(!reply){
         oops.notif('回复不能为空！');
         return;
      }
      
      var replyList = $('.reply-list', $(this).parent());
      $.ajax({
         url: '/qa/answer/crud',
         type: 'PUT',
         dataType: 'json',
         data: $.toJSON({
            content: reply,
            question_id: qid
         }),
         success: function(id){
            oops.notif('回复成功！');
            answer_input.val('');
            $.getJSON('/qa/answer/crud/'+id, null, function(data){
               var answer = data[0];
               var profile = oops.tryGetProfileFromCache(answer.fields.publisher);
               console.info(profile);
               var answerLi = $('<li><img src="/static/images/profile/' + answer.fields.publisher + '" height="16" width="16" alt="no pic" /><a href="/profile/' + answer.fields.publisher + '">' + profile.name + '</a> 说：' + answer.fields.content + '<span class="date">' + answer.fields.publish_time + '</span></li>');
               answerLi.hide().appendTo(replyList).slideDown();
            });
         },
         error: function(){
            oops.oops('无法回复！');
         }
      });
   });
});
