import React from "react";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }
      
    render() {
        return (
            <div className="container">
                <h4>Kanban Board</h4>
            </div>
        );
    }
}