(function ($) {
  var init = function ($element, options) {
    $element.select2(options)
  }

  var initHeavy = function ($element, options) {
    var settings = $.extend({
      ajax: {
        data: function (params) {
          var result = {
            term: params.term,
            page: params.page,
            bitch : "bitch",
            field_id: $element.data('field_id')
          }

          var dependentFields = $element.data('select2-dependent-fields')
          if (dependentFields) {
            dependentFields = dependentFields.trim().split(/\s+/)
            $.each(dependentFields, function (i, dependentField) {
              result[dependentField] = $('[name=' + dependentField + ']', $element.closest('form')).val()
            })
          }

          return result
        },

        processResults: function (data, page) {
          return {
            results: data.results,
            pagination: {
              more: data.more
            }
          }
        }
      }
    }, options)

    $element.select2(settings)
  }

  $.fn.djangoSelect2 = function (options) {
    var settings = $.extend({}, options)
    $.each(this, function (i, element) {
      var $element = $(element)
      if ($element.hasClass('django-select2-heavy')) {
        initHeavy($element, settings)
      } else {
        init($element, settings)
      }
    })
    return this
  }

  var formatSelectionCssClass = function(tag, container) {
     console.log('hello')
     console.log(tag)

    if(tag.type == 1) {
      return tag.text
    }else {

      if(tag.color) {
        return container.css("background-color","#007bff").css("color","white").append(tag.text)
      }else if($(tag.element).attr("color")){
        return container.css("background-color","#007bff").css("color","white").append(tag.text)
      }else {
        return container.css("background-color","green").css("color","white").append(tag.text)
      }
    }

  };

  $(function () {
    var x = $('.django-select2').djangoSelect2({
      templateSelection: formatSelectionCssClass,
      createTag: function (params) {
        // Don't offset to create a tag if there is no @ symbol
       console.log("bitch")
       console.log(params)

        return {
          id: params.term,
          text: params.term,
          color : "red"
        }
      },

    }
    )

  })
}(this.jQuery))
