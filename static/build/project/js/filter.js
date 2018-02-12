$(document).ready(function(){

    var array = "["
    var temp;
    var selectkeyword = $('#id_selectKeywords')
    var keyword = $('#id_keywords')

    var filterform = $('.pj-filter-form')

   $('form').submit(function(e){
      console.log($('#id_keywords').val())
   })

   Ladda.bind( 'input[type=submit]' );

   $('.pj-filter-click').click(function(e){
     if(filterform.hasClass('active')){
       filterform.removeClass("active")
       $(this).text("Show Filters")
     }else {
       filterform.addClass("active")
       $(this).text("Hide Filters")
     }
   })


})
