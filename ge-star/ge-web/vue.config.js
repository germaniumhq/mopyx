const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');
const path = require('path');

function resolve(dir) {
    const result = path.join(__dirname, dir);
    console.log(`${dir} -> ${result}`);

    return result;
}

module.exports = {
    configureWebpack: {
        /*
        resolve: {
            alias: {
                '@': resolve('src'),
                '@components': resolve('src/components'),
                '@node': resolve('node_modules'),
            },
        },
        */
        plugins: [
            new MonacoWebpackPlugin(),
        ],
    },
};

