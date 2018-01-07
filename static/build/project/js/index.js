var fastSelectInstance;
var recommended = []

var stopword = ["your","a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

var punctuations = ["!","#","$","%","&",'(',')',",",":",";","<","=",">","@","[","]","_"]
//var punctuations = []
/*var keywords = ["apple store","play store","git","github","big data","virtual machine","user interface",'data structure',"ssh","ethernet","keyboard","graphic","windows","object-oriented","xml","text editor","i/o","toolkit","files","email","bluetooth","torrent","compiler","logic","natural language","virtual reality","augmented reality","ransomware","virus","security","malware","algebra","gui","user interface","3d graphic","3d printing","software","hardware","hard drive","blog","database","mysql","postgresl","mongodb","schema","document","social media","facebook","twitter","instragram","open source","piracy","library","libraries","protocol","search","cloud computing","aws","amazon","android","samsung","bootstrap","operating system","wordspace","linux","microsoft","macosx","wifi","ip address","dns","cyberbullying","environment","hospital","natural language processing","html","css","javscript","bootstrap","management system","c language","supercomputer","algorithm","big data","node.js","angular.js","oracle","eclipse","nuclear","data structures","greedy algorithm","dynamic programming","machine learning","concurrency","cryptography","php","api","javascript","web","network","programming language","c++","java","python","dataset"] */
var keywords = []


function insertKeyword(text) {
   text = decodeURIComponent(text)
   fastSelectInstance.fastsearch.options.onItemSelect(null,{value:text,text:text,selected:false},fastSelectInstance.fastsearch)
}

function common(text) {
   var str = []
   for(var i = 0;i<keywords.length;i++) {
     console.log(i)
     for(var j = 0;j<text.length;j++) {
       console.log(j)
       const temp = keywords[i]
       console.log(text[j] + " " + temp)
       if(text[j].indexOf(temp) > -1) {
          str.push(temp)
          j = text.length
       }
     }
   }


   console.log(str)

   return str

}
function extract(text) {
  /*
  const opts = {stopwords: stopword};
  console.log(opts)
  var str = rake.generate(text,opts)
  recommended = str
  console.log(str)

  return str */


  var str = []
  var temp = []

  var str = nlp(text).nouns().out("array")
  temp = common(str)
  if(temp.length > 20) {
    recommended =temp
  }else {
    recommended = temp.concat(str).splice(0,20)
  }

}

function generateResultId(container, data) {
  var id = container.id + '-result-';

  id += Utils.generateChars(4);

  if (data.id != null) {
    id += '-' + data.id.toString();
  } else {
    id += '-' + Utils.generateChars(4);
  }
  return id;
}
function _normalizeItem(item) {
  if (!$.isPlainObject(item)) {
    item = {
      id: item,
      text: item
    };
  }

  item = $.extend({}, {
    text: ''
  }, item);

  var defaults = {
    selected: false,
    disabled: false
  };

  if (item.id != null) {
    item.id = item.id.toString();
  }

  if (item.text != null) {
    item.text = item.text.toString();
  }

  if (item._resultId == null && item.id && this.container != null) {
    item._resultId = this.generateResultId(this.container, item);
  }

  return $.extend({}, defaults, item);
}


function item($option) {
    var data = {};

    data = $.data($option[0], 'data');

    if (data != null) {
      return data;
    }

    if ($option.is('option')) {
      data = {
        id: $option.val(),
        text: $option.text(),
        disabled: $option.prop('disabled'),
        selected: $option.prop('selected'),
        title: $option.prop('title')
      };
    } else if ($option.is('optgroup')) {
      data = {
        text: $option.prop('label'),
        children: [],
        title: $option.prop('title')
      };

      var $children = $option.children('option');
      var children = [];

      for (var c = 0; c < $children.length; c++) {
        var $child = $($children[c]);

        var child = item($child);

        children.push(child);
      }

      data.children = children;
    }


    data = _normalizeItem(data);
    data.element = $option[0];

    $.data($option[0], 'data', data);

    return data;
  }


function current(callback) {
  var data = [];
  $('select#id_keywords').find(':selected').each(function () {
    var $option = $(this);
    var option = item($option);
    console.log("item")
    console.log(option)
    option["type"] = $option.data("type") || $option.type
    data.push(option);
  });
  console.log(data)

  callback(data);
}

function select(text,selectData) {
  console.log("test select ")
  var data = {id : text,text:text,value:text}
  data.selected = true;


  current(function (currentData) {
      console.log(currentData)
      var val = [];

      data = [data];
      data.push.apply(data, currentData);
      console.log(data)

      console.log(val)
      for (var d = 0; d < data.length; d++) {
        var id = data[d].id;
        console.log(typeof(id))
        if (id) {
          if ($.inArray(id, val) === -1) {
            val.push(id);
          }
        }else {
          val.push(id)
        }

      }

     var $select = $('select#id_keywords')
     var optionExists = false;
      for (var i = 0; i < val.length; i++) {
        if(!selectData.exists) {
          optionExists = ($('select#id_keywords option[value="' + val[i] + '"]').length > 0);
        }else {
          optionExists = ($('select#id_keywords option[value="' + selectData.id + '"]').length > 0);
        }
        if(!optionExists)
        {
          if(!selectData.exists) {
            console.log('!exists')
            $select.append("<option selected value='"+ val[i] +"' data-select2-tag='true' color='blue'>"+decodeURIComponent(val[i])+"</option>");
          }else {
            $select.append("<option data-type=" +  selectData.type + " selected value='"+ selectData.id +"' data-select2-tag='true'>"+decodeURIComponent(val[i])+"</option>");
            val[i] = selectData.id
          }
        }
      }



      $('select#id_keywords').val(val);
      console.log("$('select#id_keywords').val(val);")
      console.log($('select#id_keywords').val())
      $('select#id_keywords').trigger('change');
    });

}


function select3(text) {
  $.ajax({
    url : '/project/CheckKeywordExists',
    method : 'GET',
    data : {keyword : text},
    success : function(data)  {
       console.log(data)
       select(text,data)
    },
    error : function() {

    }
  })
}

  $(document).ready(function(){
    var root = $('.recommended').find('span')
    var globalTimeout = null;
    var array = "["
    var temp;
    var keyword = $('#id_keywords')
    /*keyword.select2({
      ajax:{
        "url" : "/project/ajax",
        type : "GET",
        delay: 500,
        closeOnSelect: false,
        data : function(params) {
          console.log(params)
          return {
            term : params.term,
            page : params.page || 0,
            page_limit : 10
          }
        },
        processResults : function(data,page){
          var more = (page * 10) < data.total;
          console.log(data.keyword)
          return {
            results : $.map(data.keyword,function(item,i){
              console.log(i)
              return {
                text : item.text,
                id : item.value
              }
            }
          ),
          more : more
          }
        }
      }
    })
    /*
    var my_list = keyword.val().split(",")
    my_list = keyword.val().split(",")
    for(var i = 0;i<my_list.length;i++) {
       if(my_list[i] !== "") {
         console.log(my_list[i])
         temp = my_list[i]
         array+= '{"text":"' + temp + '","value":"' + temp + '"},'
       }
    }
    array = array.slice(0, -1);
    if(array.length > 1) {
      array+="]"
    }

    keyword.attr("data-initial-value",array)
     fastSelectInstance = new $.Fastselect(keyword.get(0), {
      loadOnce: true,
      userOptionAllowed: true,
      "url" : "/project/ajax",
      parseData: function(data) {
         return data.keyword
      },
      onItemSelect : function(self, $item, model, self, fastsearch) {
        console.log('onItemSelect')
      },
      onItemCreate : function() {
        console.log('onItemCreate')
      },
    });

    $.ajax({
      method : 'GET',
      url : '/project/ajax/getKeywords/',
      data : {},
      success : function(data) {
        console.log(data)
        keywords = data.keywords
      },
      error : function(err) {
        keywords = []
      }
    })
   */



   Ladda.bind( 'input[type=submit]' );

    $('textarea[name="summary"]').on('keyup',function(){

          if(globalTimeout != null) clearTimeout(globalTimeout);
          globalTimeout =setTimeout(function(){
            extract($('#id_summary').val())
            root.empty()
            for(var i = 0;i<recommended.length;i++) {

              var temp = '<a onClick=select3(\'' + encodeURIComponent(recommended[i]) + '\')>'+ recommended[i] + '</a>'
              console.log(temp)
              root.append(temp)
            }
            //extract($('#id_summary').val())

          },500);
    })
  })
