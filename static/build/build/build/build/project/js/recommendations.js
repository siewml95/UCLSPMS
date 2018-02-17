$(document).ready(function(){
  var $recommendations = $('.recommendations')
  var target = document.getElementById('recommendations');
  var spinner = new Spinner({top:'150%',left:"25%",radius : 5,color:'#000'}).spin(target);
  console.log(spinner)
  var id = $('input[name="id"]').val()
  if(!id) {
    id = 0;
  }
  $.ajax({
    method : 'GET',
    url : '/user/ajax/getIndexRecommendations',
    data : {id:id},
    success : function(data) {
       console.log(data.recommendations)

       $.each(data.recommendations,function(index,recommendation){
          $recommendations.append('<tr><td><a style="display:block;" ' + ' href="/project/single/' + recommendation.slug + '">' + recommendation.title + '</a></td></tr>')
       })
       spinner.stop()
       //$.each(data.keywords,function(index,keyword){
      //   $recommendations.append('<a style="display:block;" ' + ' href="/project/single/' + keyword.slug + '">' + keyword.title + '</a>')
      // })
    },
    error : function(err) {
      spinner.stop()
      //console.log( $('input[name="id"]').val())
    }
  })
})
