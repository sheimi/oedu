/**
 * Javascript for new user group popup.
 * author: kavinyao
 * revision: 1
 */
$(document).ready(function(){
    var candidateList = $('#candidate-list');
    
    oops.notif('加载用户列表ing');
    $.getJSON('/search/user/all', null, function(data){
        $.each(data, function(index, user){
            var userLi = $(makeUserLi(user));
            userLi.hide()
            .appendTo(candidateList)
            .slideDown()
            .draggable({
                helper: 'clone',
                appendTo: 'body',
                zIndex: 1990
            });
        });
    });
    
    function makeUserLi(user){
        var profile = oops.tryGetProfileFromCache(user.pk);
        return '<li class="group-popup-target"><span class="id">' + user.pk + '</span><span class="avatar"><img src="/static/images/profile/' + user.pk + '" width="16" height="16" /></span><span class="njuid">' + profile.nju_id + '</span><span class="name">' + profile.name + '</span><p class="clear"></p></li>';
    };
    
    $('#filter-input').keyup(function(e){
        var keyword = $(this).val();
        $('#candidate-list li').each(function(index){
            var name = $('span.name', $(this)).html();
            if(name.indexOf(keyword) === -1){
                $(this).slideUp();
            }else{
                $(this).slideDown();
            }
        });
    });
    
    $('#range-filter').click(function(e){
        var start = parseInt($('#range-start').val(), 10);
        var end = parseInt($('#range-end').val(), 10);
        
        if(!start || !end || start > end){
            oops.oops('请输入正确的值！');
            return;
        }
        
        $('#candidate-list li').each(function(index){
            var njuid = parseInt($('span.njuid', $(this)).html(), 10);
            console.info(njuid);
            if(njuid >= start && njuid <= end){
                $(this).slideDown();
            }else{
                $(this).slideUp();
            }
        });
    });
    
    $('#group-submit').click(function(e){
        e.preventDefault();
        
        var groupname = $('#groupname').val();
        if(!groupname){
            oops.oops('请输入组名！');
            return;
        }
        
        $.fancybox.showActivity();
        $.ajax({
            url: '/core/usergroup/crud',
            type: 'PUT',
            dataType: 'json',
            data: $.toJSON({description: groupname}),
            success: function(gid){
                var user_list = [];
                $('#selected-list li').each(function(index){
                    var id = $('span.id', $(this)).html();
                    user_list.push(id);
                });
                
                $.ajax({
                    url: '/core/usergroup/crud/'+gid,
                    type: 'POST',
                    dataType: 'json',
                    data: $.toJSON({
                        operation: 'add',
                        users: user_list
                    }),
                    success: function(data){
                        $.fancybox.hideActivity();
                        oops.notif('创建分组成功！');
                        $.fancybox.close();
                    },
                    error: function(){
                        $.fancybox.hideActivity();
                        oops.notif('创建分组失败！');
                    }
                });
            },
            error: function(){
                $.fancybox.hideActivity();
                oops.oops("创建分组失败，分组可能已经存在");
            }
        });
    });
});