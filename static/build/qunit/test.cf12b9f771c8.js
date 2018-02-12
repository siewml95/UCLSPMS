alert('hello')
QUnit.test( "hello test", function( assert ) {
  assert.ok( 1 == "1", "Passed!" );
});

QUnit.test( "hello test", function( assert ) {
  assert.ok( 1 == "2", "Passed!" );
});
alert("bye")
