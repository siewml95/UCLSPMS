class Rake {
  constructor(text, stopwordsList) {
    this.text = text;
    this.stopwords = stopwordsList;
    this.regexExpression = this.buildRegex();
  }

  buildRegex() {
    return this.stopwords.join('|');
  }

  removeStopWords(sentence) {
    const regExp = this.regexExpression;
    const r = regExp.substring(0, regExp.length - 1);
    const reg = new RegExp(`\\b(?:${r})\\b`, 'ig');
    const filteredSentence = sentence.replace(reg, '|').split('|');
    console.log(filteredSentence)
    return filteredSentence;
  }

  splitTextToSentences(text) {
    const sentences = text.match(/[^.!?:,\\]+/g);
    const filteredSentences = sentences.filter(s => s.replace(/  +/g, '') !== '');
    return filteredSentences;
  }

  generatePhrases(sentenceList) {
    const reg = /['!"“”’#$%&()*+,\-./:;<=>?@[\\\]^_`{|}~']/g;
    const phrases = sentenceList.map(s => this.removeStopWords(s));
    const phraseList = phrases.map(phrase => phrase
      .filter(phr => (phr.replace(reg, '') !== ' ' && phr.replace(reg, '') !== ''))
      .map(phr => phr.trim()),
    );
    console.log('phraselist')
    console.log(phrases)
    console.log(phraseList)
    const flattenedList = [].concat(...phraseList);
    console.log(flattenedList)

    return flattenedList;
  }

  // Generates score for each word.
  calculateKeywordScores(phraseList) {
    const wordFreq = {};
    const wordDegree = {};
    const wordScore = {};
    console.log(phraseList)
    phraseList.forEach((phrase) => {
      var wordList = phrase.match(/[,.!?;:/‘’“”]|\b[0-9a-z']+\b/gi);
      if(!wordList) {
        wordList = []
      }



      var wordListDegree = 0;

      try {
         wordListDegree = wordList.length
      }catch(err) {
         wordListDegree = 0
      }

      console.log(wordList)

      wordList.forEach((word) => {
        if (wordFreq[word]) {
          wordFreq[word] += 1;
        }
        else {
          wordFreq[word] = 1;
        }
        if (wordDegree[word]) {
          wordDegree[word] += wordListDegree;
        }
        else {
          wordDegree[word] = wordListDegree;
        }
      });
    });

    Object.values(wordFreq).forEach((freq) => { wordDegree[freq] += wordFreq[freq]; });
    Object.keys(wordFreq).forEach((i) => { wordScore[i] = wordDegree[i] / (wordFreq[i] * 1.0); });
    return wordScore;
  }

  // Generates score for each phrase based on the word scores.
  calculatePhraseScores(phraseList, wordScore) {
    const phraseScores = {};
    phraseList.forEach((phrase) => {
      phraseScores[phrase] = 0;
      let candidateScore = 0;
      var wordList = phrase.match(/(\b[^\s]+\b)/g);
      if(!wordList) {
        wordList = []
      }




      wordList.forEach((word) => { candidateScore += wordScore[word]; });
      phraseScores[phrase] = candidateScore;
    });
    return phraseScores;
  }

  sortPhrases(obj) {
    return Object.keys(obj).sort((a, b) => obj[b] - obj[a]);
  }

  generate() {
    const sentenceList = this.splitTextToSentences(this.text);
    const phrasesList = this.generatePhrases(sentenceList);
    const wordScores = this.calculateKeywordScores(phrasesList);
    const phraseScores = this.calculatePhraseScores(phrasesList, wordScores);
    const result = this.sortPhrases(phraseScores);
    return result;
  }
}

module.exports = Rake;
