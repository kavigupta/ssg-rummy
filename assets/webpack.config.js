const path = require('path');

const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: {
        "game": ['./src/game.js']
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, '..', 'ssg_rummy_server', 'static', 'dist'),
        clean: true
    },
    resolve: {
        // Add '.ts' and '.tsx' as resolvable extensions.
        extensions: ["", ".webpack.js", ".web.js", ".ts", ".tsx", ".js"],
    },
    module: {
        rules: [
            // All files with a '.ts' or '.tsx' extension will be handled by 'ts-loader'.
            { test: /\.tsx?$/, loader: "ts-loader" },
            // All output '.js' files will have any sourcemaps re-processed by 'source-map-loader'.
            { test: /\.js$/, loader: "babel-loader" },
        ],
    },
    devtool: 'inline-source-map',
};
