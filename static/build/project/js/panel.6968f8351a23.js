$(document).ready(function() {

    $('.list-group-item').each(function(e){
      console.log('.list-group-item')
      $input = $(this)
      $target = $input.find('input')
      console.log($target.val())
      if($target.val()) {
        $target = $input.find('.panel-item')
        $target.attr('display','block')
      }
    })

    $('[id^=detail-]').hide();
    $('.toggle').click(function() {
        $input = $( this );
        $target = $('#'+$input.attr('data-toggle'));
        $target.slideToggle();
    });
});
