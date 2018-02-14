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
      return tag.text.toLowerCase().trim()
    }else {

      if(tag.color) {
        return container.css("background-color","#007bff").css("color","white").append(tag.text.toLowerCase().trim())
      }else if($(tag.element).attr("color")){
        return container.css("background-color","#007bff").css("color","white").append(tag.text.toLowerCase().trim())
      }else {
        return container.css("background-color","green").css("color","white").append(tag.text.toLowerCase().trim())
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
          id: params.term.toLowerCase().trim(),
          text: params.term.toLowerCase().trim(),
          color : "red"
        }
      },
      matcher : function (params, data) {
        console.log('matcher')
        // If there are no search terms, return all of the data
        if ($.trim(params.term) === '') {
            return data;
        }
        var myTerm = $.trim(params.term);
        // `params.term` should be the term that is used for searching
        // `data.text` is the text that is displayed for the data object
        if (data.text.toLowerCase().indexOf(myTerm.toLowerCase()) > -1) {
            // You can return modified objects from here
            // This includes matching the `children` how you want in nested data sets
            return data;
        }

        // Return `null` if the term should not be displayed
        return null;
        }

    }
    )

  })
}(this.jQuery))
