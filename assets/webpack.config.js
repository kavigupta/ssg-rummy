const path = require('path');

module.exports = {
    entry: { "game": ['./src/game.js'], "reorderable-list": ['./src/reorderable-list.js'] },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, '..', 'ssg_rummy_server', 'static', 'dist'),
        clean: true
    },
};
