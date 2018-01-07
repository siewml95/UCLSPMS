$(document).ready(function() {

    $('.list-group-item').each(function(e){
      console.log('.list-group-item')
      $input = $(this)
      $target = $input.find('input')
      if($target.val()) {
        $target = $input.find('.panel-item')
        $target.slideToggle()
      }
    })

    $('[id^=detail-]').hide();
    $('.toggle').click(function() {
        $input = $( this );
        $target = $('#'+$input.attr('data-toggle'));
        $target.slideToggle();
    });
});
