
QUnit.test("test common function",function(assert){
  var str = nlp("Use Keiko to implement a simple language that is purely object-oriented. Study the compromises that must be made to get reasonable performance, comparing your implementation with Smalltalk, Ruby or Scala.").nouns().out("array")
  var texts = common(str)
  console.log("QUNIT")
  console.log(texts)
  assert.ok( texts.length == 0, "Passed!" );
})

QUnit.test("test extract function",function(assert){
  extract("Use Keiko to implement a simple language that is purely object-oriented. Study the compromises that must be made to get reasonable performance, comparing your implementation with Smalltalk, Ruby or Scala.")
  assert.ok( recommended[0] == "keiko", "Passed!" );
})

QUnit.test("test extract function with no punctuation",function(assert){
  extract("Use Keiko to implement a simple language that is purely object-oriented. Study the compromises that must be made to get reasonable performance, comparing your implementation with Smalltalk, Ruby or Scala.")
  for(var i = 0;i<stopword.length;i++) {
    for(var j = 0;j<recommended.length;j++) {
      assert.ok(recommended[j] != stopword[i])
    }
  }
})


QUnit.test("test getKeywords function",function(assert) {
  getKeywords()
  assert.ok(keywords instanceof Array,"Passed!")
})

QUnit.test("test select function",function(assert){
  var arr = select("keiko",{exists:false},selectCB)
  assert.ok(arr[0] == "keiko","Passed!")
})

QUnit.test("test select function for exist keyword",function(assert){
  var arr = select("data",{exists: true, id: 10, active: true, type: 1},selectCB)
  assert.ok(arr[0] == "10","Passed!")
})

QUnit.test("test selectCB function",function(assert){
  var arr = selectCB("keiko",{exists:false},[])
  assert.ok(arr[0] == "keiko","Passed!")
})

QUnit.test("test selectCB function for exists keyword",function(assert){
  var arr = selectCB("data",{exists: true, id: 10, active: true, type: 1},[])
  assert.ok(arr[0] == "data","Passed!")
})

QUnit.test("test _normalizeItem function",function(assert){
  var item = _normalizeItem('text')
  console.log(item)
  assert.ok(item["id"] == "text","Passed!")
  assert.ok(item["text"] == "text","Passed!")
})

QUnit.test("test _normalizeItem function with json",function(assert){
  var item = _normalizeItem({id: 'text','text':'text'})
  console.log(item)
  assert.ok(item["id"] == "text","Passed!")
  assert.ok(item["text"] == "text","Passed!")
})

QUnit.test("test item function",function(assert){
  var ite = item($('<option value="10" data-type="1">data</option>'));
  console.log(ite)
  assert.ok(ite["id"] == 10,"Passed!")
  assert.ok(ite["text"] == "data","Passed!")
})

QUnit.test("test item function type 2",function(assert){
  var ite = item($('<option value="text" data-type="2">data</option>'));
  console.log(ite)
  assert.ok(ite["id"] == "text","Passed!")
  assert.ok(ite["text"] == "data","Passed!")
})
