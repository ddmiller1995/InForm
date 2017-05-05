import React from "react";
import {Link, IndexLink} from "react-router";
import YouthFormsColumn from "./youth-forms-column.jsx";
import "whatwg-fetch";
import {postRequest, getRequest} from '../util.js';

let form_data = [];
const statuses = ["pending", "in progress", "done"]

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            form_types: []
        };

        this.changeFormStatusHandler = this.changeFormStatusHandler.bind(this);
        this.getColumns = this.getColumns.bind(this);
    }

    componentDidMount() {
        let response = getRequest("/api/form-type", this, "form_types");

    }

    changeFormStatusHandler(form, direction) {
        let visitID = this.props.currentYouth.youth_visits[0].youth_visit_id;
        let data = new FormData();
        console.log(form);
        data.append("form_id", form.id);
        
        let index = statuses.indexOf(form.status) + direction;
        if(index > -1 && index < statuses.length) {
            data.append("status", statuses[index]);
            postRequest('/api/visit/' + visitID + '/change-form-status', data);
        } else {
            throw 'Error: Unexcepted status type - ' + form.status;
        }
    }

    getColumns() {
        let columns = [];
        let forms_by_status = {};
        for(let i = 0; i < statuses.length; i++) {
            forms_by_status[statuses[i]] = [];
        }
        for(let i = 0; i < form_data.length; i++) {
            let form = form_data[i];
            forms_by_status[form.status].push(form);
        }
        for(let i = 0; i < statuses.length; i++) {
            let status = statuses[i];
            columns.push(<YouthFormsColumn key={status} status={status} handler={this.changeFormStatusHandler} 
                                           formTypes={this.state.form_types} forms={forms_by_status[status]} />);
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