$.validator.addMethod('filesize', function (value, element, param) {
    return this.optional(element) || (element.files[0].size <= param)
}, 'File size must be less than {0}');


$.validator.addMethod( "extension", function( value, element, param ) {
        	param = typeof param === "string" ? param.replace( /,/g, "|" ) : "png|jpe?g";
        	return this.optional( element ) || value.match( new RegExp( "\\.(" + param + ")$", "i" ) );
}, $.validator.format( "Please enter a value with a valid extension." ) );


$(".form-file").validate({
  rules: {
    image: {
      extension: "jpeg,png",
      filesize: 1000000
    },
    avatar: {
      extension: "jpeg,png",
      filesize: 1000000
    },
    resume: {
      extension: "pdf",
      filesize: 1000000
    },
  },
  messages: {
    image: {
      extension: "Please enter a value with a valid extension",
      filesize: "Maximum file size is 1 MB"
    },
    avatar: {
      extension: "Please enter a value with a valid extension",
      filesize: "Maximum file size is 1 MB"
    },
    resume: {
      extension: "Please enter a pdf file",
      filesize: "Maximum file size is 1 MB"
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
});

$('.form-file input[type="file"]').on('change',function(e) {
  $('.form-file').valid()
})
