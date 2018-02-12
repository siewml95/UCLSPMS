$(document).ready(function(){
  var $recommendations = $('.project-recommendations')
  var target = document.getElementById('project-recommendations');
  var spinner = new Spinner({top:'150%',left:"25%",radius : 5,color:'#000'}).spin(target);
  $.ajax({
    method : 'GET',
    url : '/project/ajax/getDetailRecommendations',
    data : {id: $('input[name="id"]').val()},
    success : function(data) {
       console.log(data)
       $.each(data.keywords,function(index,keyword){
         $recommendations.append('<a style="display:block;" ' + ' href="/project/single/' + keyword.slug + '">' + keyword.title + '</a>')
       })
       spinner.stop()
    },
    error : function(err) {
      spinner.stop()
      console.log( $('input[name="id"]').val())
    }
  })

  $('#myModal button[name="submit"]').click(function(e){
    e.preventDefault()
    var l = Ladda.create(this);
    l.start()
    $.ajax({
      method : 'GET',
      url : '/user/ajax/sendInterest',
      data : {id: $('input[name="id"]').val(),description: $('textarea[name="description"]').val()},
      success : function(data) {
         if(data.amount) {
           $('#modalBtn').html("Send Interest " + data.amount)
           toastr.success('Succesfully sent!')
         }
         l.stop()
         $('#myModal').modal('toggle')
      },
      error : function(err) {
        toastr.error(err.responseJSON.error)
        l.stop()
      }
    })
  })
  

})
