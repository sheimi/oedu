/**
 * Javascript for new user group popup.
 * author: kavinyao
 * revision: 3
 */
$(document).ready(function(){
    var candidateList = $('#candidate-list');
    
    $('ul li').draggable({
        helper: 'clone',
        appendTo: 'body',
        zIndex: 1990
    });
    
    $('#selected-list').droppable({
        accept: '#usergroup-popup li',
        hoverClass: 'hover',
        drop: function(event, ui){
            var dropped_li = ui.draggable;
            $(dropped_li).appendTo($(this)).attr('style', 'position: relative;');
        }
    });
    
    $('#candidate-list').droppable({
        accept: '#usergroup-popup li',
        hoverClass: 'hover',
        drop: function(event, ui){
            var dropped_li = ui.draggable;
            $(dropped_li).appendTo($(this)).attr('style', 'position: relative;');
        }
    });
});