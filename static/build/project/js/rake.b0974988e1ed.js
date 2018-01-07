var collections = require("pycollections")
var tokenizer = require('string-tokenizer')
const groupBy = require('./groupby');
const product = require('./product');
const chain = require('./chain');
const Set = require('set')
var $ = require('jquery')

// tokenize(str)
// extracts semantically useful tokens from a string containing English-language sentences
// @param {String}    the string to tokenize
// @returns {Array}   contains extracted tokens

function wordpunct_tokenize(str) {

   var punct='\\['+ '\\!'+ '\\"'+ '\\#'+ '\\$'+              // since javascript does not
             '\\%'+ '\\&'+ '\\\''+ '\\('+ '\\)'+             // support POSIX character
             '\\*'+ '\\+'+ '\\,'+ '\\\\'+ '\\-'+             // classes, we'll need our
             '\\.'+ '\\/'+ '\\:'+ '\\;'+ '\\<'+              // own version of [:punct:]
             '\\='+ '\\>'+ '\\?'+ '\\@'+ '\\['+
             '\\]'+ '\\^'+ '\\_'+ '\\`'+ '\\{'+
             '\\|'+ '\\}'+ '\\~'+ '\\]',

       re=new RegExp(                                        // tokenizer
          '\\s*'+            // discard possible leading whitespace
          '('+               // start capture group #1
            '\\.{3}'+            // ellipsis (must appear before punct)
          '|'+               // alternator
            '\\w+\\-\\w+'+       // hyphenated words (must appear before punct)
          '|'+               // alternator
            '\\w+\'(?:\\w+)?'+   // compound words (must appear before punct)
          '|'+               // alternator
            '\\w+'+              // other words
          '|'+               // alternator
            '['+punct+']'+        // punct
          ')'                // end capture group
        );

   // grep(ary[,filt]) - filters an array
   //   note: could use jQuery.grep() instead
   // @param {Array}    ary    array of members to filter
   // @param {Function} filt   function to test truthiness of member,
   //   if omitted, "function(member){ if(member) return member; }" is assumed
   // @returns {Array}  all members of ary where result of filter is truthy

   function grep(ary,filt) {
     var result=[];
     for(var i=0,len=ary.length;i++<len;) {
       var member=ary[i]||'';
       if(filt && (typeof filt === 'Function') ? filt(member) : member) {
         result.push(member);
       }
     }
     return result;
   }

   return grep( str.split(re));   // note: filter function omitted
                                   //       since all we need to test
                                   //       for is truthiness
} // end tokenize()

class Rake {
  constructor(stopwords, punctuations) {

    this.stopwords = stopwords
    this.punctuations = punctuations

    if(this.stopwords) {
      this.stopwords = []
    }

    if(this.punctuations) {
      this.punctuations = []
    }

    this.to_ignore = new Set(this.stopwords.concat(this.punctuations))

    this.frequency_dist = null
        this.degree = null
        this.rank_list = null
        this.ranked_phrases = null
  }

  extract_keywords_from_text(text) {
    const sentences = text.split(" ")
    this.extract_keywords_from_sentences(sentences)
  }

  extract_keywords_from_sentences(sentences) {
    const phrase_list = this._generate_phrases(sentences)
    this._build_frequency_dist(phrase_list)
    this._build_word_co_occurance_graph(phrase_list)
    this._build_ranklist(phrase_list)
  }

  get_ranked_phrases() {
     return this.ranked_phrases
  }

  get_rannked_pharases_with_scores() {
    return this.rank_list
  }

  get_word_frequency_distribution() {
    return this.frequency_dist
  }

  get_word_degrees() {
    return this.degree
  }

  _build_frequency_dist(phrase_list) {
    this.frequency_dist = new collections.DefaultDict(function(){return 0});
    for (word in chain(phrase_list)) {
      this.frequency_dist[word] +=1
    }
  }

  _build_word_co_occurance_graph(phrase_list) {
    var co_occurance_graph =  new collections.DefaultDict(function(){return 0});
       $.each(phrase_list,function(index,phrase){
         console.log('phrase ')
         console.log( phrase)

          $.each(product(phrase,phrase),function(index,result){
            co_occurance_graph[result[0]][result[1]] += 1
          })
       })
       this.degree =  new collections.DefaultDict(function(){return 0});
       for(key in co_occurance_graph) {
         this.degree[key] = sum(co_occurance_graph[key].values())
       }
    }



   _build_ranklist(phrase_list) {
       this.rank_list = []
       var that = this;
       var rank = 0.0
       for(phrase in phrase_list) {
         rank = 0.0
         for(word in phrase) {
           rank += 1.0 * this.degree[word] / this.frequency_dist[word]
           this.rank_list.push((rank,' '.join(phrase)))
         }
       this.rank_list.sort().reverse()
       $.each(this.rank_list,function(index,ph){
         that.ranked_phrases.push(ph[1])
       })
      }
   }

   _generate_phrases(sentences) {
     var phrase_list = new Set()
     var word_list = []
     var that = this
     console.log(sentences)

     $.each(sentences,function(index,sentence){
        console.log(sentence)
        $.each(wordpunct_tokenize(sentence),function(index,word){
          word_list.push(word.toLowerCase())
          console.log("word_list")

          console.log(word_list)

        })
        console.log('get_phrase_list_from_words')
        console.log(that._get_phrase_list_from_words(word_list))
        $.each(that._get_phrase_list_from_words(word_list),function(index,item){
          phrase_list.add(item)
        })
     })
     console.log("phrase_list")
     console.log(phrase_list)
     return phrase_list
   }

  lamda(x) {
    for(var i = 0;i<this.to_ignore.length;i++) {
       if(x == this.to_ignore[i]) {
         return true
       }
    }
    return false
  }


  _get_phrase_list_from_words(word_list) {
    var phrase_list = []
    var groups = groupBy(word_list,this.lambda)
    console.log('groups')
    console.log(groups)
    $.each(groups,function(index,item){
      if(item[0]) {
        //phrase_list.push(item[1])
      }
    })
    return phrase_list
  }
}

module.exports = Rake
