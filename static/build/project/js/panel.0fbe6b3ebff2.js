$(document).on('click', '.panel-heading span.clickable', function(e){
         var $this = $(this);
         if(!$this.hasClass('panel-collapsed')) {
             $this.parents('.panel').find('.panel-body').slideUp();
             $this.addClass('panel-collapsed');
             $this.find('i').removeClass('glyphicon glyphicon-minus-sign').addClass('glyphicon glyphicon-plus-sign');
         } else {
             $this.parents('.panel').find('.panel-body').slideDown();
             $this.removeClass('panel-collapsed');
             $this.find('i').removeClass('glyphicon glyphicon-plus-sign').addClass('glyphicon glyphicon-minus-sign');
         }
     })
