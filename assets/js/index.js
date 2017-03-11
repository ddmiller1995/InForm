let React = require('react')
let ReactDOM = require('react-dom')
import 'whatwg-fetch';

let Hello = React.createClass ({
    render: function() {
        return (
            <h1>
            Hello, React!
            </h1>
        )
    }
})

ReactDOM.render(<Hello />, document.getElementById('container'))