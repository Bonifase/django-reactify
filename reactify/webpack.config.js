const path = require("path");
const webpack = require("webpack");
const { styles } = require( '@ckeditor/ckeditor5-dev-utils' );

module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "./static/writing"),
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /ckeditor5-[^/\\]+[/\\]theme[/\\]icons[/\\][^/\\]+\.svg$/,
        use: [ 'raw-loader' ]
      },
      {
        test: /ckeditor5-[^/\\]+[/\\]theme[/\\].+\.css$/,
        use: [
            {
                loader: 'style-loader',
                options: {
                    injectType: 'singletonStyleTag',
                    attributes: {
                        'data-cke': true
                    }
                }
            },
            {
                loader: 'postcss-loader',
                options: styles.getPostCssConfig( {
                    themeImporter: {
                        themePath: require.resolve( '@ckeditor/ckeditor5-theme-lark' )
                    },
                    minify: true
                } )
            }
        ]
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
    ],
  },
  optimization: {
    minimize: true,
  },
  plugins: [
    new webpack.DefinePlugin({
        'process.env.NODE_ENV' : JSON.stringify('development')
    })
  ],
};