/**
 * JavaScript for ajax-editable profile location fields.
 * author: kavinyao
 * revision: 1
 */
$(document).ready(function() {
    var old_value;
    $("#profile-info-location").keydown(function(e){
        if(e.which === 13){
            //it's enter
            $(this).focusout()
        }
    }).focusin(function() {
        $(this).addClass("edit").select();
        old_value = $(this).val();
    }).focusout(function() {
        $(this).removeClass("edit");
        
        var regex = /profile-info-(\w+)/;
        var id = $(this).attr('id');
        var modified_value = $(this).val();
        var field = id.match(regex)[1];
        
        if(field === null){
            //something bad happened
            oops.notif('You ain\'t to do bad!');
            return;
        }
        console.info(field + '[old:' + old_value + ']');
        console.info(field + '[new:' + modified_value + ']');
        if(old_value !== modified_value){
            var data = {};
            data[field] = modified_value;
            console.info(data);
            $.ajax({
                url: '/core/crud/',
                type: 'POST',
                data: $.toJSON(data),
                success: function(data){
                    oops.notif('修改位置成功！');
                },
                error: function(){
                    oops.notif('Oops，修改位置失败:(');
                }
            });
        }
    });
});