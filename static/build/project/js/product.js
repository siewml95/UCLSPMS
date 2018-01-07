

function iter(iterable) {
  var args = Array.prototype.slice.call(arguments, 1);
  if (iterable[Symbol.iterator]) {
    return iterable[Symbol.iterator](...args);
  } else if (typeof iterable === 'object' && 'next' in iterable) {
    return iterable;
  } else if (typeof iterable === 'function') {
    return iter(iterable(...args));
  } else if (typeof iterable === 'object') {
    return (function* objectIter(obj) {
      var keys = Object.keys(obj);
      for (var i = 0; i < keys.length; i++) {
        yield [keys[i], obj[keys[i]]];
      }
    }(iterable));
  }
  throw new Error('The argument is not a generator or iterator');
}

function map(func, iterable) {
  function* curriedMap(i) {
    let c = 0;
    for (let item of iter(i)) {
      yield func(item, c++);
    }
  }
  if (iterable) {
    return curriedMap(iterable);
  }
  return curriedMap;
}


function product() {
  var iters = Array.prototype.map.call(arguments, function (i) { return iter(i); });

  function* multiply(iterable1, iterable2) {
    for (var item1 of iterable1) {
      for (var item2 of iterable2) {
        yield item1.concat(item2);
      }
    }
  }

  if (iters.length === 0) {
    return function* () {};
  } else {
    var currentIter = [[]];
    for (var it of iters) {
      currentIter = multiply(currentIter, Array.from(it));
    }
    return currentIter;
  }
}

module.exports = product;
