/**
 * Javascript for global site instant messaging.
 * author: kavinyao
 * revision: 22
 * dependency: oops-global.js
 */

$(document).ready(function(){
    $('div.chat-window span.min-button').live('click', function(event){
        event.stopPropagation();
        $(this).parents('div.chat-window').hide('slow');
    });
    
    $('div.chat-window span.close-button').live('click', function(event){
        event.stopPropagation();
        oops.im.remove_chat_window($(this).parents('div.chat-window').attr('id'));
    });
    
    $('div.chat-window p.title').live('mousedown', function(){
        $(this).parent().css({opacity: 0.75});
    }).live('mouseup', function(){
        $(this).parent().css({opacity: 1});
    });
    
    $('div.chat-window textarea.message-input').live('keydown', function(event){
        if(event.which == 13){
            event.preventDefault();
            $(this).next().trigger('click');
        }
    });
    
    $('div.chat-window input.message-submit').live('click', function(event){
        event.preventDefault();
        event.stopPropagation();
        
        var id_string = $(this).parents('div.chat-window').attr('id');
        var chat_target_id = oops.im.getIdFromIdString(id_string);
        var message_field = $(this).prev();
        var message = message_field.val();
        message_field.val('');//empty input
        
        oops.im.sendMessage(chat_target_id, message);
    });
    
    $('ul#chat-window-list span.close').live('click', function(event){
        event.stopPropagation();
        var identifier = $(this).parent().attr('class');
        oops.im.remove_chat_window(identifier);
    });
    
    $('ul#chat-window-list li').live('click', function(event){
        event.stopPropagation();
        
        var idString = $(this).attr('class');
        oops.im.dock_click(idString);
    });
    
    $('ul#online-user li').live('click', function(event){
        var target_id = parseInt($('span.user-id', $(this)).text());
        var target_name = $('span.user-name', $(this)).text();
        
        var targets = [];
        targets.push(target_id);
        var session = oops.im.create_session(targets);
        oops.im.constructChatWindow(session, target_name);
        $(this).parent().slideUp();
    });
   
   $("input#chat-target").focusout(function(event){
    $('ul#online-user').slideUp();
    $(this).val('');
   }).keyup(function(event){
    if(event.which === 8){
        //backspace
        return;
    }
    
    var keyword = $(this).val();
    if(!keyword || keyword.length < 1){
        //too short
        return;
    }
    
    $.ajax({
        url: '/search/user',
        data: {realname: keyword},
        dataType: 'json',
        success: function(data){
            $('ul#online-user').remove();
            
            if(data.length === 0){
                oops.oops('木有匹配的用户');
                return;
            }
            
            var list = '<ul id="online-user">';
            $.each(data, function(i, x){
                var profile = oops.tryGetProfileFromCache(x.pk);
                list += '<li><span class="user-id">' + x.pk + '</span><span class="user-name">' + profile.name + '</span></li>';
            });
            list += '</ul>';
            var list_html = $(list);
            list_html.css({
                position: 'fixed',
                left: $('input#chat-target').offset().left + 'px',
                bottom: '30px',
                'z-index': 1000
            }).hide();
            $('div#bottom-bar').append(list_html);
            list_html.slideDown();
        },
        error: function(){
            oops.oops('Oops，得不到列表呀:(');
        }
    })
   });
   
   oops.im.start_polling();
});