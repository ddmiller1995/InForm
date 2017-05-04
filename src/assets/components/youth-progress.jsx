import React from "react";
import {Link, IndexLink} from "react-router";
import YouthFormsColumn from "./youth-forms-column.jsx";
import "whatwg-fetch";
import {postRequest, getRequest} from '../util.js';

let form_data = [];
const statuses = ["Pending", "In Progress", "Done"]

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            form_types: []
        };

        this.getColumns = this.getColumns.bind(this);
    }

    componentDidMount() {
        let response = getRequest("/api/form-type", this, "form_types");

    }

    getColumns() {
        let columns = [];
        let forms_by_status = {};
        for(let i = 0; i < statuses.length; i++) {
            forms_by_status[statuses[i].toLowerCase()] = [];
        }
        for(let i = 0; i < form_data.length; i++) {
            let form = form_data[i];
            forms_by_status[form.status].push(form);
        }
        for(let i = 0; i < statuses.length; i++) {
            let status = statuses[i];
            columns.push(<YouthFormsColumn key={status} status={status} formTypes={this.state.form_types} forms={forms_by_status[status.toLowerCase()]} />);
        }
        return columns;
    }
      
    render() {
        if(this.props.currentYouth.youth_visits) {
            form_data = this.props.currentYouth.youth_visits[0].forms;
        }
        let columns = this.getColumns();


        return (
            <div className="container">
                <div className="board">
                    {columns}
                </div>
            </div>
        );
    }
}