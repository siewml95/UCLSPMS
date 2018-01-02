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

class groupby {
  constructor(iterable,key) {
    if(!key) {
      key = function(x) {return x}
    }
    this.keyfunc = key
    this.it = iter(iterable)
    this.tgtkey = null;
    this.currkey = null;
    this.currvalue = null
  }

  __iter__() {
    return this;
  }

  next() {
    while(this.currkey == this.tgtkey) {
      
    }
    while self.currkey == self.tgtkey:
        self.currvalue = next(self.it)    # Exit on StopIteration
        self.currkey = self.keyfunc(self.currvalue)
    self.tgtkey = self.currkey
    return (self.currkey, self._grouper(self.tgtkey))
  }
}

class groupby(object):
    # [k for k, g in groupby('AAAABBBCCDAABBB')] --> A B C D A B
    # [list(g) for k, g in groupby('AAAABBBCCD')] --> AAAA BBB CC D
    def __init__(self, iterable, key=None):
        if key is None:
            key = lambda x: x
        self.keyfunc = key
        self.it = iter(iterable)
        self.tgtkey = self.currkey = self.currvalue = object()
    def __iter__(self):
        return self
    def next(self):
        while self.currkey == self.tgtkey:
            self.currvalue = next(self.it)    # Exit on StopIteration
            self.currkey = self.keyfunc(self.currvalue)
        self.tgtkey = self.currkey
        return (self.currkey, self._grouper(self.tgtkey))
    def _grouper(self, tgtkey):
        while self.currkey == tgtkey:
            yield self.currvalue
            self.currvalue = next(self.it)    # Exit on StopIteration
            self.currkey = self.keyfunc(self.currvalue)
function* groupby(iterable, key) {
  key = key || function (key) { return key; };
  console.log('key groupby')
  iterable = iter(iterable);
  console.log('iterable' + ite)

  var currentItem;
  var currentKey, previousKey;

  function* group() {
    while (true) {
      yield currentItem.value;
      currentItem = iterable.next();
      if (currentItem.done) return;
      currentKey = key(currentItem.value);
      if (previousKey !== currentKey) {
        return;
      }
    }
  };

  currentItem = iterable.next();

  while (true) {
    if (currentItem.done) return;
    currentKey = key(currentItem.value);
    if (previousKey !== currentKey) {
      previousKey = currentKey;
      yield [currentKey, group()];
    }
    else {
      currentItem = iterable.next();
    }
  }
}

module.exports = groupby;
