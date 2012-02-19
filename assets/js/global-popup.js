/**
 * JavaScript for global site popup window feature.
 * author: kavinyao
 * revision: 4
 * dependency: fancybox.js
 *             (home-made)util.js
 * 
 * usage: <a class="ajax-popup" href="{url}">Description</a>
 */

//use closure to prevent global variables
(function(){
    $('a.ajax-popup').fancybox({
        transitionIn: 'elastic',
        transitionOut: 'elastic',
        overlayOpacity: 0.1,
        opacity: true
    });
    
    $('.popup-cancel').live('click', function(){
        $.fancybox.close();
        oops.notif('发送取消');
    });
    
    $('#popup-anno-send').live('click', function(event){
        event.preventDefault();
        
        if($('#select-single').attr('checked')){
            var data = {
                title: $('#popup-anno-title').val(),
                grade: $('#popup-anno-receiver').val(),
                content: $('#popup-anno-content').val()
            }
            
            $.ajax({
                url: '/anno/crud',
                type: 'PUT',
                dataType: 'json',
                data: $.toJSON(data),
                success: function(data){
                    $.fancybox.close();
                    oops.notif('通知发送成功！');
                },
                error: function(){
                    oops.oops('发送失败:(');
                }
            });
        }else{
            var users = oops._popup_users;
            console.info(users);
            var data = {
                title: $('#popup-anno-title').val(),
                users: users,
                content: $('#popup-anno-content').val()
            }
            
            $.ajax({
                url: '/anno/pub_anno',
                type: 'PUT',
                dataType: 'json',
                data: $.toJSON(data),
                success: function(data){
                    $.fancybox.close();
                    oops.notif('通知发送成功！');
                },
                error: function(){
                    oops.oops('发送失败:(');
                }
            });
        }
    });
    
    $('#popup-mail-send').live('click', function(event){
        event.preventDefault();
        
        if($('#select-single').attr('checked')){
            var data = {
                title: $('#popup-mail-title').val(),
                to_user: $('#target-pk').val(),
                message: $('#popup-mail-content').val()
            }
            
            $.ajax({
                url: '/mail/crud',
                type: 'PUT',
                dataType: 'json',
                data: $.toJSON(data),
                success: function(data){
                    $.fancybox.close();
                    oops.notif('站内信发送成功！');
                },
                error: function(){
                    oops.oops('发送失败:(');
                }
            });
        }else{
            var users = oops._popup_users;
            console.info(users);
            var data = {
                title: $('#popup-mail-title').val(),
                to_users: users,
                message: $('#popup-mail-content').val()
            }
            
            $.ajax({
                url: '/mail/send/mul',
                type: 'PUT',
                dataType: 'json',
                data: $.toJSON(data),
                success: function(data){
                    $.fancybox.close();
                    oops.notif('站内信发送成功！');
                },
                error: function(){
                    oops.oops('发送失败:(');
                }
            });
        }
    });
    
    $('#popup-question-send').live('click', function(event){
        event.preventDefault();
        
        var data = {
            title: $('#popup-question-title').val(),
            receiver: $('#target-pk').val(),
            content: $('#popup-question-content').val()
        }
        
        $.ajax({
            url: '/qa/crud',
            type: 'PUT',
            dataType: 'json',
            data: $.toJSON(data),
            success: function(data){
                $.fancybox.close();
                oops.notif('提问发送成功！');
            },
            error: function(){
                oops.oops('发送失败:(');
            }
        });
    });
    
    $('#popup-rent-send').live('click', function(event){
        event.preventDefault();
        
        var data = {
            title: $('#popup-rent-equipname').val(),
            to_teacher: $('#target-pk').val(),
            content: $('#popup-rent-content').val()
        }
        
        $.ajax({
            url: '/rent/crud',
            type: 'PUT',
            dataType: 'json',
            data: $.toJSON(data),
            success: function(data){
                $.fancybox.close();
                oops.notif('申请发送成功！');
            },
            error: function(){
                oops.oops('发送失败:(');
            }
        });
    });
    
    $('#popup-feedback-send').live('click', function(event){
        event.preventDefault();
        
        var data = {
            title: $('#popup-feedback-title').val(),
            receiver: $('#target-pk').val(),
            content: $('#popup-feedback-content').val()
        }
        
        $.ajax({
            url: '/feedback/crud',
            type: 'PUT',
            dataType: 'json',
            data: $.toJSON(data),
            success: function(data){
                $.fancybox.close();
                oops.notif('反馈发送成功！');
            },
            error: function(){
                oops.oops('发送失败:(');
            }
        });
    });
})();