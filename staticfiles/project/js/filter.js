$(document).ready(function(){

    var array = "["
    var temp;
    var selectkeyword = $('#id_selectKeywords')
    var keyword = $('#id_keywords')

    var filterform = $('.pj-filter-form')
    /*var my_list = keyword.val().split(",")

    for(var i = 0;i<my_list.length;i++) {
         if(my_list[i] !== "") {
           console.log(my_list[i])
           temp = my_list[i]
           array+= '{"text":"' + temp + '","value":"' + temp + '"},'
         }
    }
    array = array.slice(0, -1);
    if(array.length > 1) {
        array+="]"
    }
    //keyword.val("")
    console.log(array) */
    /*selectkeyword.select2({
      ajax:{
        "url" : "/project/ajax",
        type : "GET",
        delay: 500,
        closeOnSelect: false,
        data : function(params) {
          console.log(params)
          return {
            term : params.term,
            page : params.page || 0,
            page_limit : 10
          }
        },
        processResults : function(data,page){
          var more = (page * 10) < data.total;
          console.log(data.keyword)
          return {
            results : $.map(data.keyword,function(item,i){
              console.log(i)
              return {
                text : item.text,
                id : item.value
              }
            }
          ),
          more : more
          }
        }
      }
    }) */
    /*keyword.attr("data-initial-value",array)
    keyword.fastselect({
      "url" : "/project/ajax",
      parseData: function(data) {
         return data.keyword
      },
    }); */


   $('form').submit(function(e){
     //e.preventDefault()
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
