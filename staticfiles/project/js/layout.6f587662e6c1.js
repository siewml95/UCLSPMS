
$('#bugModal button[name="submit"]').click(function(e){
  e.preventDefault()
  var l = Ladda.create(this);
  l.start()
  var $form = $('#bugModal form')

  console.log('hello')
  $form.validate({
    submitHandler: function(form) {
      console.log('submitHandler')
      content = $('textarea[name="content"]').val()
      $.ajax({
        method : 'GET',
        url : '/user/ajax/sendBug',
        data : {content: content},
        success : function(data) {
           toastr.success('Succesfully sent!')
           l.stop()
           $('#bugModal').modal('toggle')
        },
        error : function(err) {
          toastr.error(err.responseJSON.error)
          l.stop()
        }
      })
    },
    invalidHandler: function(event, validator) {
  // 'this' refers to the form\
  l.stop()
  var errors = validator.numberOfInvalids();
  if (errors) {
    var message = errors == 1
      ? 'You missed 1 field. It has been highlighted'
      : 'You missed ' + errors + ' fields. They have been highlighted';
    $("div.error span").html(message);
    $("div.error").show();
  } else {
    $("div.error").hide();
  }
},

  highlight: function(element) {
      $(element).closest('.form-group').addClass('has-error');
  },
  unhighlight: function(element) {
      $(element).closest('.form-group').removeClass('has-error');
  },
   errorElement: 'span',
   errorClass: 'help-block',
   errorPlacement: function(error, element) {
       if(element.parent('.input-group').length) {
           error.insertAfter(element.parent());
       } else {
           error.insertAfter(element);
       }
   }

  })
  if($form.valid()) {
    console.log('submitHandler')
    content = $form.find('textarea[name="content"]').val()
    content = $form.find('input[name="email"]').val()

    $.ajax({
      method : 'GET',
      url : '/user/ajax/sendBug',
      data : {email : email,content: content},
      success : function(data) {
         toastr.success('Succesfully sent!')
         l.stop()
         $('#bugModal').modal('toggle')
      },
      error : function(err) {
        toastr.error(err.responseJSON.error)
        l.stop()
      }
  })
}
})
