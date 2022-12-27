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
            { test: /\.tsx?$/, loader: "ts-loader" },
            { test: /\.js$/, loader: "babel-loader" },
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader"]
            },

        ],
    },
    devtool: 'inline-source-map',
};
