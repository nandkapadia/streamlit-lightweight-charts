const path = require('path');
const CompressionPlugin = require('compression-webpack-plugin');

module.exports = function override(config, env) {
  if (env === 'production') {
    config.optimization = {
      ...config.optimization,
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all',
          },
          lightweightCharts: {
            test: /[\\/]node_modules[\\/]lightweight-charts[\\/]/,
            name: 'lightweight-charts',
            chunks: 'all',
          },
        },
      },
    };

    config.plugins.push(
      new CompressionPlugin({
        filename: '[path][base].gz',
        algorithm: 'gzip',
        test: /\.(js|css|html|svg)$/,
        threshold: 10240,
        minRatio: 0.8,
      })
    );
  }

  return config;
}; 