QUnit.test( "hello test", function( assert ) {
  assert.ok( 1 == "1", "Passed!" );
});

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

QUnit.test("test current function",function(assert){
  var arr = select("keiko",{exists:False},selectCB)
  assert.ok(keywords == [],"Passed!")

})
