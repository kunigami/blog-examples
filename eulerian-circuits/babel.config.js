const presets = [
  [
    "@babel/env",
    {
      targets: {
        firefox: "60",
        chrome: "67",
        safari: "11.1"
      },
      useBuiltIns: "usage"
    }
  ]
];

const plugins = [
  "@babel/plugin-proposal-class-properties",
  "@babel/plugin-transform-flow-strip-types"
];

module.exports = { presets, plugins };
