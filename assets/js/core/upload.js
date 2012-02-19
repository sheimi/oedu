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
    $('#dropzone').css({
        lineHeight: '8em',
        textAlign: 'center',
        border: '2px dashed #aaaaaa',
        margin: '8px 15px 8px 15px',
        display: 'none'
    }).dropup({
        url:'/core/upload_image',
        params: {func: 'upload'},
        on_complete: function() {
            var t = $('#user-avatar').attr("src");
            t += '?' + new Date().getTime();
            $('#user-avatar').attr("src", t);
        },
        on_start: function($index, $file) {

        },
        on_progress: function($index, $file, $per) {

        },
        on_finish: function($index, $file, $json) {

        },
        on_g_enter: function() {
            $('#dropzone').show();
            $('#user-avatar').hide();
        },
        on_enter: function() {
            $('#dropzone').css({
                backgroundColor: '#dddddd'
            });
        },
        on_leave: function() {
            $('#dropzone').css({
                backgroundColor: 'transparent'
            });
        },
        on_g_leave: function() {
            $('#dropzone').hide();
            $('#user-avatar').show();
        },
    });
});
