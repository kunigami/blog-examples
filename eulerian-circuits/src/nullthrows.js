// @flow

function nullthrows<T>(value: ?T, message: string): T {
  if (value == null) {
    throw new Error(message);
  }
  return value;
}

module.exports = nullthrows;
