var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')
const isReachable = require('is-reachable');

let ip = 'localhost';

module.exports = {
    //the base directory (absolute path) for resolving the entry option
    context: __dirname,
    entry: [
        `webpack-dev-server/client?http://${ip}:3000`,
        'webpack/hot/only-dev-server',
        './assets/index'
    ],
    
    output: {
        path: path.resolve('./assets/bundles/'), 
        //naming convention webpack should use for your files
        filename: '[name]-[hash].js', 
        publicPath: `http://${ip}:3000/assets/bundles/`
    },
    
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}), 
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoEmitOnErrorsPlugin(), 
        //makes jQuery available in every module
        new webpack.ProvidePlugin({ 
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery' 
        })
    ],
    
    module: {
        rules: [
            {
                test: /\.jsx?$/, 
                exclude: /node_modules/, 
                use: [
                    {   
                        loader: "react-hot-loader/webpack"
                    },
                    {
                        loader: "babel-loader",
                        options: {
                            presets: ['react']
                        }
                    }
                ],
            },
            {
                test: /\.css$/,
                use: [ 'style-loader', 'css-loader' ]
            }
        ]
    },
    
    resolve: {
        //tells webpack where to look for modules
        modules: ['node_modules', 'bower_components'],
        //extensions that should be used to resolve modules
        extensions: ['.js', '.jsx'] 
    }   
}


isReachable('192.168.99.100:8000').then(reachable => {
    if (reachable) {
        ip = '192.168.99.100';
    }

    module.exports.output.publicPath = `http://${ip}:3000/assets/bundles/`;

    module.exports.entry = [
        `webpack-dev-server/client?http://${ip}:3000`,
        'webpack/hot/only-dev-server',
        './assets/index'
    ];
});