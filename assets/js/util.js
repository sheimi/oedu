/**
 * Small utilities for oedu project.
 * author: kavinyao
 * reversion: 2
 */

// Array Remove - By John Resig (MIT Licensed)
Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
};

//center plugin for jquery
//put the target element center of the screen
(function($){
    $.fn.center = function () {
      return this.each(function(){
        var $this = $(this);
        //$this.css("display", "block");
        $this.css("position", "absolute");
        $this.css("top", ($(window).height() - $this.height())/2 + $(window).scrollTop() + "px");
        $this.css("left", ($(window).width() - $this.width())/2 + $(window).scrollLeft() + "px");
      });
    };
})(jQuery);

//topcenter plugin for jquery
//put the target element top-center of the screen
(function($){
    $.fn.topcenter = function () {
      return this.each(function(){
        var $this = $(this);
        //$this.css("display", "block");
        $this.css("position", "fixed");
        $this.css("top", "0px");
        $this.css("left", ($(window).width() - $this.width())/2 + $(window).scrollLeft() + "px");
      });
    };
})(jQuery);