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
