QUnit.test( "hello test", function( assert ) {
  assert.ok( 1 == "1", "Passed!" );
});

QUnit.test("test common function",function(assert){
  getKeywords()
  var texts = common("Use Keiko to implement a simple language that is purely object-oriented. Study the compromises that must be made to get reasonable performance, comparing your implementation with Smalltalk, Ruby or Scala.")
  console.log(texts)
  assert.ok( 1 == "1", "Passed!" );

})
