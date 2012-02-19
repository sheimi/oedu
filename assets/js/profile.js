/**
 * @author sony
 */
$(document).ready(function(){
	$('.messages-area').hide();
	$('.leave-messages-area').hide();
	$('.feedback-area').hide();
	$('.profile-question-area').hide();
	$('.anno-feedback-area').hide();
	$('.personal-info-area').hide();
	$('.agenda-area').hide();
	
	var current_ontop_tag = $('#news');
	var current_ontop_area = $('.news-area');
	
	$('#news').click(function(event){
		current_ontop_tag.removeClass('current-selected');
		$(this).addClass('current-selected');
		current_ontop_tag = $(this);
		
		current_ontop_area.hide();
		$('.news-area').show();
		current_ontop_area = $('.news-area');
	});
	
	$('#release-status').click(function(event){
		current_ontop_tag.removeClass('current-selected');
		$(this).addClass('current-selected');
		current_ontop_tag = $(this);
		
		current_ontop_area.hide();
		$('.status-area').show();
		current_ontop_area = $('.status-area');
	});
	$('#leave-messages').click(function(event){
		current_ontop_tag.removeClass('current-selected');
		$(this).addClass('current-selected');
		current_ontop_tag = $(this);
		
		current_ontop_area.hide();
		$('.leave-messages-area').show();
		current_ontop_area = $('.leave-messages-area');
	});
	$('.feedback').click(function(event){
		current_ontop_tag.removeClass('current-selected');
		$(this).addClass('current-selected');
		current_ontop_tag = $(this);
		
		current_ontop_area.hide();
		$('.feedback-area').show();
		current_ontop_area = $('.feedback-area');
	});
	$('.question').click(function(event){
		current_ontop_tag.removeClass('current-selected');
		$(this).addClass('current-selected');
		current_ontop_tag = $(this);
		
		current_ontop_area.hide();
		$('.profile-question-area').show();
		current_ontop_area = $('.profile-question-area');
	});
	//$('.anno-feedback').click(function(event){
	//	current_ontop_tag.removeClass('current-selected');
	//	$(this).addClass('current-selected');
	//	current_ontop_tag = $(this);
	//	
	//	current_ontop_area.hide();
	//	$('.anno-feedback-area').show();
	//	current_ontop_area = $('.anno-feedback-area');
	//});
	$('.personal-info').click(function(event){
		current_ontop_tag.removeClass('current-selected');
		$(this).addClass('current-selected');
		current_ontop_tag = $(this);
		
		current_ontop_area.hide();
		$('.personal-info-area').show();
		current_ontop_area = $('.personal-info-area');
	});
	$('.agenda').click(function(event){
		current_ontop_tag.removeClass('current-selected');
		$(this).addClass('current-selected');
		current_ontop_tag = $(this);
		
		current_ontop_area.hide();
		$('.agenda-area').show();
		current_ontop_area = $('.agenda-area');
	});
});