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
                <div className="kanban-board">
                    <div className="col1"></div>
                    <div className="col2"></div>
                    <div className="col3"></div>
                </div>
            </div>
        );
    }
}