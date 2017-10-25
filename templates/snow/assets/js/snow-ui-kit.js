
/* =================================
Tooltips        
=================================== */
$(function () {
  $('[data-toggle="popover"]').popover()
})

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

/* =================================
Parallax        
=================================== */
$(document).ready(function(){
	// Parallax        
    if (($(window).width() >= 1024)) {
        $(".parallax").parallax("50%", -0.4);
    } 
	// Parallax Section BG
	var pageSection = $(".full-bg");
    pageSection.each(function(indx){
        
        if ($(this).attr("data-background")){
            $(this).css("background-image", "url(" + $(this).data("background") + ")");
        }
    });
});


/* =================================
Header switch class        
=================================== */
$(function() {
    var navbar = $("#main-nav");
    $(window).scroll(function() {    
        var scroll = $(window).scrollTop();
    
        if (scroll >= 300) {
            navbar.removeClass('bg-transparent').addClass('bg-light');
            navbar.removeClass('navbar-dark').addClass('navbar-light');
        } else {
            navbar.addClass('bg-transparent').removeClass('bg-light');
            navbar.addClass('navbar-dark').removeClass('navbar-light');
        }
    });
});

/* =================================
Datepicker      
=================================== */
$('input.date-picker').datepicker({
    format: "dd/mm/yyyy",
    forceParse: false,
    autoclose: true,
    todayHighlight: true
});

$('.input-daterange').datepicker({
    format: "dd/mm/yyyy",
    forceParse: false,
    autoclose: true,
    todayHighlight: true
});

$('.input-group.date').datepicker({
    format: "dd/mm/yyyy",
    forceParse: false,
    autoclose: true,
    todayHighlight: true
});