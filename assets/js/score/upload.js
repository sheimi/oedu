/**
 * JavaScript for global site popup window feature.
 * author: kavinyao
 * revision: 4
 * dependency: fancybox.js
 *             (home-made)util.js
 *
 * usage: <a class="ajax-popup" href="{url}">Description</a>
 */
$(document).ready( function() {
    $('#score-dropzone').css({
        lineHeight: '3em',
        textAlign: 'center',
        border: '2px dashed #aaaaaa',
        display: 'none'
    }).dropup({
        url:'/score/upload_xlrd',
        params: {func: 'upload'},
        on_complete: function() {
            get_course_list();
        },
        on_start: function($index, $file) {

        },
        on_progress: function($index, $file, $per) {

        },
        on_finish: function($index, $file, $json) {

        },
        on_g_enter: function() {
            $('#score-dropzone').show();
        },
        on_enter: function() {
            $('#score-dropzone').css({
                backgroundColor: '#dddddd'
            });
        },
        on_leave: function() {
            $('#score-dropzone').css({
                backgroundColor: 'transparent'
            });
        },
        on_g_leave: function() {
            $('#score-dropzone').hide();
        },
    });
    function get_course_list() {
        $.ajax({
            url:'/score/course_list/all', 
            type: 'GET', 
            dataType: 'json',
            success: function(data_list) {
                $(".course-item").remove();
                for (var i = 0; i < data_list.length; i++) {
                    var str='<li class="course-item"><a href="/score/course/' + data_list[i].pk + '" class="ajax"><div class="course-li">';
                    str += '<div class="course-name">' 
                        + data_list[i].fields.name + '</div>';
                    str += '<div class="course-grade">' + data_list[i].fields.grade + '</div>';
                    str += '<div class="grade-point">' + data_list[i].fields.grade_point + '</div>';
                    str += '<div><div class="clear" style="clear: both;"></div></a></li>'
                    $('#course-list').append(str);
                }
                $('a.ajax').fancybox({
                    transitionIn: 'elastic',
                    transitionOut: 'elastic',
                    overlayOpacity: 0.1,
                    opacity: true,
                    autoDimensions: false,
                    width: 500,
                    height: 400
                });
                $('.course-li').hover(function() {
                    $(this).css({
                        background: 'rgba( 255, 255, 190, 10)'
                    });
                }, function() {
                    $(this).css({
                        background: 'transparent'
                    });
                });
            }
        });;
         
    }
    
    get_course_list();

});
