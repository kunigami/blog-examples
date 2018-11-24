// @flow

/**
 * Thin wrapper around an array to add the ability to record a state
 * of the traversal.
 */
class StatefulArray<T> {
  _list: Array<T>;
  _index: number;

  constructor(list: ?Array<T>) {
    this._list = list || [];
    this._index = 0;
  }

  push(element: T): this {
    this._list.push(element);
    return this;
  }

  current(): ?T {
    if (this._index >= this._list.length) {
      return null;
    }

    return this._list[this._index] || null;
  }

  next(): ?T {
    if (this._index >= this._list.length) {
      return null;
    }
    this._index += 1;
    return this._list[this._index];
  }

  getArray(): Array<T> {
    return this._list;
  }
}

module.exports = StatefulArray;
