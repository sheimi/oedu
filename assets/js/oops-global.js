/**
 * Foundation JavaScript for oedu-by-oops website.
 * function provided: instant messaging/notification
 * author: kavinyao
 * revision: 14
 * dependency: jquery.ui.draggable.js
 *             (home-made) util.js
 */

/* ====== API Documentation =====
 *
 * Chat API dependency: div#chat-window-container
                        ul#chat-window-list
 * Status API dependency: ul#status-list
 * Tag API dependency: ul#tag-list
 */
(function(window){
    var _profile_cache = [];
    
    $('.input-tip').live('focus', function(){
        $(this).val('').removeClass('input-tip');
    });
    
    $('a.status-reply').live('click', function(e){
      e.preventDefault();
      
      if($(this).hasClass('already-loaded')){
        var replyList = $('ul.reply-list', $(this).parent().parent());//FRAGILE!
        var input = replyList.next();
        var submit = input.next();
        
        if($(this).hasClass('wrapped-up')){
            $(this).removeClass('wrapped-up');
            $('li', replyList).slideDown();
            input.slideDown();
            submit.slideDown();
            input.focus();
        }else{
            $(this).addClass('wrapped-up');
            $('li', replyList).slideUp();
            input.slideUp();
            submit.slideUp();
        }
        
        return;
      }
      
      $(this).addClass('already-loaded');
      
      $.fancybox.showActivity();
      var numSpan = $('span.reply-num', this); //keep it
      var url = $(this).attr('href');
      var replyList = $('ul.reply-list', $(this).parent().parent());
      $.getJSON(url, {}, function(data){
        numSpan.before('(').after(')');
        numSpan.html(data.length);
        $.each(data, function(index, reply){
           var replyLi = $(oops.makeReplyLi(reply));
           replyLi.hide();
           replyList.append(replyLi);
           replyLi.slideDown();
        });
        var reply_input = $('<textarea class="status-reply-input" rows="1" cols="35" /><input class="status-reply-button" type="button" value="回复" />');
        //reply_input.hide();
        replyList.after(reply_input);
        //reply_input.slideDown();
        replyList.next().focus(); //fragile!
        
        $.fancybox.hideActivity();
      });
   });
   
   $('.status-reply-input').live('keydown', function(e){
      if(e.which !== 13){
         //not interested
         return;
      }
      
      $(this).next().trigger('click'); //fragile!  
   });
   
   $('input.status-reply-button').live('click', function(){
      var reply_input = $(this).prev();
      var reply = reply_input.val(); //fragile!
      
      if(reply.length > 140){
         oops.notif('回复得在140字内哦，亲~');
         return;
      }
      
      if(!reply){
         //empty reply
         oops.notif("Oops，回复不能为空");
         return;
      }
      
      var replyList = $(this).siblings('ul.reply-list');//fragile!
      var numSpan = $('span.reply-num', $(this).parent());
      console.info(numSpan);
      var url = $('a.status-reply', $(this).siblings('.publish-time')).attr('href');//fragile!
      var status_id = url.match(/\/status\/replylist\/(\d+)/)[1];
      //console.info(status_id);
      
      oops.notif("努力传送ing");
      $.fancybox.showActivity();
      $.ajax({
         url: '/status/reply/crud',
         type: 'PUT',
         data: $.toJSON({content: reply, status: status_id}),
         dataType: 'json',
         success: function(rid){
            $.fancybox.hideActivity();
            oops.notif("回复状态成功");
            reply_input.val('');
            var reply_num = parseInt(numSpan.html());
            reply_num++;
            numSpan.html(reply_num);
            
            //get reply
            $.getJSON('/status/reply/crud/'+rid, {}, function(data){
               var replyLi = $(oops.makeReplyLi(data[0]));
               replyLi.hide();
               replyList.append(replyLi);
               replyLi.slideDown();
            });
         },
         error: function(){
            $.fancybox.hideActivity();
            oops.notif("Oops，回复失败 :(");
         }
        });
    });
   
    var im_manager = {
        chat_target_list: [],
        z_index: 500,
        current_on_top: -1,
        
        getIdFromIdString: function(id_string){
            var regex = /^chat-window-(\d+)$/;
            var id = id_string.replace(regex, '$1');
            return parseInt(id);
        },
        
        construct_window_if_not_exist: function(chat_target, target_name){
            var target_index = im_manager.chat_target_list.indexOf(chat_target);
            //if the target is already in list, return
            if(target_index !== -1)
                return;
            
            oops.notif('successfully!');
            
            //else, add the target to list
            im_manager.chat_target_list.push(chat_target);
            console.info(im_manager.chat_target_list);
            im_manager.constructChatWindow(chat_target, target_name);
        },
        
        constructChatWindow: function(chat_window_id, chat_target){
            //create new elements
            var identifier = 'chat-window-' + chat_window_id;
            var newWindowDiv = $('<div id="' + identifier +'" class="chat-window"><p class="title">和<span class="chat-target">' + chat_target + '</span>聊天<span class="close-button">x</span><span class="min-button">_</span></p><ul class="message-pane"></ul><textarea class="message-input"></textarea><input class="message-submit" type="submit" value="Send" /></div>');
            var newWindowDock = $('<li class="' + identifier + '">' + chat_target + '<span class="close">x</span></li>');
            
            //make chat window draggable
            //and append it to window container
            newWindowDiv.draggable({handle:"p.title"}).appendTo($("div#chat-window-container"));
            
            //add click event to dock
            //and append it to dock list
            newWindowDock.appendTo($("ul#chat-window-list"));
            im_manager.current_on_top = chat_window_id;
            newWindowDiv.css('z-index', ++im_manager.z_index).center().show('slow');
            $('.message-input', newWindowDiv).focus();
        },
        
        remove_chat_window: function(identifier){
            var chat_window = $('div#' + identifier);
            var window_dock = $('ul#chat-window-list li.' + identifier);
            //console.info(window_dock);
            var target_id = im_manager.getIdFromIdString(identifier);
            
            im_manager.chat_target_list.remove(im_manager.chat_target_list.indexOf(target_id));
    
            chat_window.remove();
            window_dock.remove();
            console.info(im_manager.chat_target_list);
        },
        
        dock_click: function(idString){
            var id = im_manager.getIdFromIdString(idString);
            var chat_window = $('div#' + idString);
            
            if(chat_window.css("display") === 'none'){
                //make sure the window appears on top
                chat_window.css('z-index', ++im_manager.z_index).center().show('slow');
                var message_list = $('ul.message-pane', chat_window);
                message_list.animate({scrollTop: message_list.attr('scrollHeight')}, 1000);
            }else if(im_manager.current_on_top !== id){
                //the current window is visible, but below the top
                //so, bring it to top
                //make sure the window appears on top
                im_manager.current_on_top = id;
                chat_window.css('z-index', ++im_manager.z_index);
            }else{
                chat_window.hide('slow');
            }
        },
        
        showMyMessage: function(data){
            updater.showMyMessage(data);
        },
        
        sendMessage: function(target_id, message){
            var data = {
                receiver: target_id,
                message: message
            };
            
            $.ajax({
                url: '/im/newmessage',
                type: 'POST',
                data: $.toJSON(data),
                dataType: 'json',
                success: function(data){
                    oops.im.showMyMessage(data);
                },
                error: function(){
                }
            });
        },
        
        start_polling: function(){
            updater.poll();
        }
    };
    
    var updater = {
        errorSleepTime: 500,
        cursor: null,
    
        poll: function() {
            args = {};
            $.ajax({
                url: "/im/update",
                type: "POST",
                dataType: "json",
                data: $.param(args),
                success: updater.onSuccess,
                error: updater.onError
            });
        },
    
        onSuccess: function(response) {
            try {
                updater.showMessage(response);
            } catch (e) {
                updater.onError();
                return;
            }
            updater.errorSleepTime = 500;
            window.setTimeout(updater.poll, 0);
        },
    
        onError: function(response) {
            updater.errorSleepTime *= 2;
            console.error("Poll error; sleeping for", updater.errorSleepTime, "ms");
            window.setTimeout(updater.poll, updater.errorSleepTime);
        },
    
        showMessage: function(message) {
            im_manager.construct_window_if_not_exist(message.sender_id, message.sender);
            updater.dispatchMessage(message.sender_id, message.sender, message.message, false);
        },
        
        showMyMessage: function(message) {
            updater.dispatchMessage(message.receiver_id, message.sender, message.message, true);
        },
        
        dispatchMessage: function(target_id, who, what, isMe){
            var hilight_class = isMe ? 'hilight-me' : 'hilight';
            var chat_window_id = 'div#chat-window-' + target_id;
            var message_list = $('ul.message-pane', chat_window_id);
            var message = $('<li><span class="' + hilight_class + '">' + who + ' 说：</span>' + what + '</li>');
            message.hide();
            message_list.append(message);
            message.show(); //speed it, to make scroll behave normally
            message_list.animate({scrollTop: message_list.attr('scrollHeight')}, 1000);
        }
    };
    
    window.oops = {
        im: im_manager,
        
        notif: function(message, delay){
            delay = typeof(delay) != 'undefined' ? delay : 2000;
            
            var notif = $('<div class="oops-top-notif">' + message + '</div>');
            notif.hide();
            notif.appendTo($('body')).topcenter();
            notif.slideDown();
            window.setTimeout(function(){
                notif.slideUp();
                //notif.remove();
            }, delay);
        },
        
        oops: function(message, delay){
            delay = typeof(delay) != 'undefined' ? delay : 2000;
            
            var notif = $('<div class="oops-top-error">' + message + '</div>');
            notif.hide();
            notif.appendTo($('body')).topcenter();
            notif.slideDown();
            window.setTimeout(function(){
                notif.slideUp();
                //notif.remove();
            }, delay);
        },
        
        getUserIdFromPath: function(){
          var idregex = /^.*\/profile(\/(\d+))?$/;
          var path = window.location.pathname;
          var raw_id = path.match(idregex)[2];
          
          if(raw_id === undefined){
            return '';
          }
          
          return raw_id;
        },
        
        makeStatusLi: function(status){
            var uid = status.fields.publisher;
            var profile = oops.tryGetProfileFromCache(uid);
            
            return '<li><div class="img"><img class="avatar" src="/static/images/profile/'+uid+'" height="40" width="40" alt="no pic" /></div><div class="content"><a href="/profile/' + uid + '">' + profile.name + '</a> 说: ' + status.fields.content +'<br /><span class="publish-time">' + status.fields.publish_time + ' <a class="status-reply" href="/status/replylist/' + status.pk + '">回复<span class="reply-num"></span></a> <a class="status-share" href="/share/status/'+status.pk+'">分享</a></span><br /><ul class="reply-list"></ul></div><div class="clear"></div></li>';
        },
       
        makeAnnoLi: function(anno){
            var publisher = oops.tryGetProfileFromCache(anno.fields.publisher)
            return '<li><a href="/anno/' + anno.pk + '/read">' + '<p>' + publisher.name + '：' + anno.fields.content + ' at ' + anno.fields.publish_time + '</p></a></li>';
        },
        
        makeReplyLi: function(reply){
            var publisher = oops.tryGetProfileFromCache(reply.fields.publisher);
            return '<li><a href="/profile/' + publisher.pk + '">' + publisher.name + '</a> 说：' + reply.fields.content + ' at ' + reply.fields.publish_time + '</li>';
        },
        
        makeShareLi: function(share){
            var uid = share.fields.publisher;
            var publisher = oops.tryGetProfileFromCache(uid);
            var type = share.fields.type;
            var s = '';
            if (type == 'link') {
                s = '<a href="' + share.fields.url +'">'+ share.fields.url +'</a>'
            } else if (type == 'status') {
                s = share.share_object.fields.content;  
            } else {
                s = share.fields.url
            }
            var str = '<li><div class="img"><img class="avatar" src="/static/images/profile/'
                    +uid+'" height="40" width="40" alt="no pic" /></div><div class="content"><a href="/profile/'
                    + uid + '">' + publisher.name + '</a> 分享了: ' + s 
                    +'<br /><span class="publish-time">' + share.fields.publish_time 
                    + '</span><br /><span class="comment">评论：'+share.fields.comment
                    +'</span></div><div class="clear"></div></li>';
            return str;
        },
        
        getShareType: function(share){
            var type = '链接';
            var url = share.url;
            if(url.indexOf('/status') === 0){
                type = '状态';
            }else if(url.indexOf('/static/images') === 0){
                type = '图片';
            }
            
            return type;
        },
        
        tryGetProfileFromCache: function(uid){
            for(var i = 0;i < _profile_cache.length;i++){
                if(_profile_cache[i].pk === uid){
                    //console.info('cache hit: ' + uid + ' at index: ' + i);
                    return _profile_cache[i];
                }
            }
            
            //console.info('cache miss: ' + uid + ', get it...');
            var p = null;
            $.ajax({
                url: '/core/crud/'+uid,
                async: false,
                dataType: 'json',
                success: function(data){
                    p = data[0];
                    //newly added profile is likely to get more
                    _profile_cache.unshift(p);
                },
                error: function(){
                    //fake one
                    p = {
                        name: 'SAMPLE',
                        username: 'NON-EXIST',
                        pk: 0
                    };
                }
            });
            
            return p;
        }
    };
})(window);