$(document).ready(function() {




    $('#button-id-reset').click(function() {
      $('[id^=detail-]').each(function() {
        $this = $(this)
        $this.find('select.django-select2').empty().trigger('change')
        $this.find('select.select.sf').val("0")

        $this.find('input').val("")
        $this.find('input').prop( "checked", false );
      })
    })
});
