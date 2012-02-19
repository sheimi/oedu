/**
 * Javascript for new user group popup.
 * author: kavinyao
 * revision: 1
 */
$(document).ready(function(){
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
        
        var user_list = [];
        $('#selected-list li').each(function(index){
            var id = $('span.id', $(this)).html();
            user_list.push(id);
        });
        
        var gid = $('#popup-group-id').val();
        $.fancybox.showActivity();
        $.ajax({
            url: '/core/usergroup/crud/'+gid,
            type: 'POST',
            dataType: 'json',
            data: $.toJSON({
                operation: 'update',
                users: user_list,
                description: groupname
            }),
            success: function(data){
                $.fancybox.hideActivity();
                oops.notif('修改分组成功！');
                $.fancybox.close();
            },
            error: function(){
                $.fancybox.hideActivity();
                oops.notif('修改分组失败！');
            }
        });
    });
});