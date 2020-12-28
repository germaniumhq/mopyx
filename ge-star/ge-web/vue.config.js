const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');
const path = require('path');

function resolve(dir) {
    const result = path.join(__dirname, dir);
    console.log(`${dir} -> ${result}`);

    return result;
}

module.exports = {
    configureWebpack: {
        resolve: {
            alias: {
                '@': resolve('src'),
                '@germanium-vue-patternfly': resolve('src/shared/germanium-vue-patternfly'),
            },
        },
        plugins: [
            new MonacoWebpackPlugin(),
        ],
    },
};

