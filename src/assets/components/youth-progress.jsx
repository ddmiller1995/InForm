import React from "react";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    // onComponentDidMount() {
    //     console.log(this.refs.col2.clientHeight);
    //     console.log(this.refs.col2.clientTop);
    //     console.log(this.refs.col2.clientLeft);
    //     console.log(this.refs.col2.clientWidth);
    // }
      
    render() {
        return (
            <div className="container">
                <div className="kanban-board">
                    <div className="col1" ref="col1"></div>
                    <div className="col2" ref="col2"></div>
                    <div className="col3" ref="col3"></div>
                </div>
            </div>
        );
    }
}