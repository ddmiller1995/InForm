var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    //the base directory (absolute path) for resolving the entry option
    context: __dirname,
    entry: [
        'webpack-dev-server/client?http://localhost:3000',
        'webpack/hot/only-dev-server',
        './assets/index'
    ],
    
    output: {
        path: path.resolve('./assets/bundles/'), 
        //naming convention webpack should use for your files
        filename: '[name]-[hash].js', 
        publicPath: 'http://localhost:3000/assets/bundles/'
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