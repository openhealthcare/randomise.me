
$(document).ready( function(){
    $('.datepicker').datepicker();

    $.fn.carousel.defaults = {
        interval: false
        , pause: 'hover'
    }

    var trigger = 'hover';
    if(window.location.search.search(/popover=click/) == 1){
        trigger = 'click'
    }
    $('.icon-question-sign').popover({trigger: 'click'})

});
