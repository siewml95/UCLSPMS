$(document).ready(function() {

    $('#id_summary option').each(function(){
      $this = $(this);
      if(!$this.attr('value')) {
        $this.remove()
      }
    })
    $('[id^=detail-]').hide();

    $('.list-group-item input.textinput').each(function(e){
       $input = $(this)

      console.log($input.val())
      if($input.val()) {
        $target = $input.closest('.panel-item')
        $target.show()
      }
    })

    $('.list-group-item select').each(function(e){
      $this = $(this).closest(".list-group-item")
      if($this.has('.select2-selection__choice').length > 0) {
        $target = $this.find('.panel-item')
        $target.show()
      }
    })

    $('.toggle').click(function() {
        $input = $( this );
        $target = $('#'+$input.attr('data-toggle'));
        $target.slideToggle();
    });

    $('#button-id-reset').click(function() {
      $('[id^=detail-]').each(function() {
        $this = $(this)
        $this.find('select.django-select2').empty().trigger('change')
        $this.find('select.select.sf').val("0")

        $this.find('input').val("")
      })
      $('[id^=detail-]').hide();

    })
});
