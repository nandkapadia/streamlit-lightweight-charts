const path = require('path')
const CompressionPlugin = require('compression-webpack-plugin')
const TerserPlugin = require('terser-webpack-plugin')

module.exports = function override(config, env) {
  if (env === 'production') {
    // Enable aggressive tree shaking
    config.optimization = {
      ...config.optimization,
      usedExports: true,
      sideEffects: false,
      minimize: true,
      moduleIds: 'deterministic',
      chunkIds: 'deterministic',
      minimizer: [
        new TerserPlugin({
          terserOptions: {
            compress: {
              drop_console: false, // Keep console.error and console.warn, remove only via pure_funcs
              drop_debugger: true,
              pure_funcs: ['console.log', 'console.info'],
              passes: 2, // Multiple compression passes
              unsafe: true, // Enable unsafe optimizations
              unsafe_comps: true,
              unsafe_Function: true,
              unsafe_math: true,
              unsafe_proto: true,
              unsafe_regexp: true,
              unsafe_undefined: true,
            },
            mangle: {
              safari10: true, // Better Safari compatibility
            },
            format: {
              comments: false,
            },
          },
          extractComments: false,
        }),
      ],
      splitChunks: {
        chunks: 'all',
        minSize: 20000,
        maxSize: 200000, // Smaller chunks for better caching
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all',
            priority: 10,
            enforce: true,
          },
          lightweightCharts: {
            test: /[\\/]node_modules[\\/]lightweight-charts[\\/]/,
            name: 'lightweight-charts',
            chunks: 'all',
            priority: 20,
            enforce: true,
          },
          react: {
            test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
            name: 'react',
            chunks: 'all',
            priority: 30,
            enforce: true,
          },
          common: {
            name: 'common',
            minChunks: 2,
            chunks: 'all',
            priority: 5,
            reuseExistingChunk: true,
            enforce: true,
          },
        },
      },
    }

    // Add compression plugin with better settings
    config.plugins.push(
      new CompressionPlugin({
        filename: '[path][base].gz',
        algorithm: 'gzip',
        test: /\.(js|css|html|svg)$/,
        threshold: 8192, // Lower threshold for more compression
        minRatio: 0.8,
        deleteOriginalAssets: false,
      })
    )

    // Enable scope hoisting and module concatenation
    config.optimization.concatenateModules = true
    
    // Set production mode explicitly
    config.mode = 'production'
    
    // Optimize module resolution
    config.resolve = {
      ...config.resolve,
      extensions: ['.tsx', '.ts', '.jsx', '.js'],
      alias: {
        ...config.resolve.alias,
        // Add any specific aliases for better tree shaking
      },
    }
  }

  return config
} 