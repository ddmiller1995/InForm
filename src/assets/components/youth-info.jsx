import React from "react";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }
      
    render() {
        console.log("youth info props: " + this.props)
        return (
            <div className="container">
                <h4>Youth Name</h4>
            </div>
        );
    }
}