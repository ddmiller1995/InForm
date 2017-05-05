import React from "react";
import {Link, IndexLink} from "react-router";
import YouthFormsColumn from "./youth-forms-column.jsx";
import "whatwg-fetch";
import {postRequest, getRequest} from '../util.js';

// let form_data = [];
const statuses = ["pending", "in progress", "done"]

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            form_types: [],
            currentYouth: {}
        };

        this.changeFormStatusHandler = this.changeFormStatusHandler.bind(this);
        this.getColumns = this.getColumns.bind(this);
    }

    componentDidMount() {
        let response = getRequest("/api/form-type", this, "form_types");
        this.setState({
            currentYouth: this.props.currentYouth
        })
        console.log(this.state.currentYouth);
        console.log(this.props.currentYouth);

    }

    changeFormStatusHandler(form, direction) {
        let visitID = this.state.currentYouth.youth_visits[0].youth_visit_id;
        let data = new FormData();
        data.append("form_id", form.form_id);
        
        let index = statuses.indexOf(form.status) + direction;
        if(index > -1 && index < statuses.length) {
            data.append("status", statuses[index]);
            postRequest('/api/visit/' + visitID + '/change-form-status/', data);
        } else {
            throw 'Error: Unexcepted status type - ' + form.status;
        }
        getRequest("/api/youth/" + this.state.currentYouth.youth_id, this, "currentYouth");
        this.forceUpdate();
    }

    getColumns() {
        let columns = [];
        let forms_by_status = {};
        for(let i = 0; i < statuses.length; i++) {
            forms_by_status[statuses[i]] = [];
        }
        if(this.state.currentYouth && this.state.currentYouth.youth_visits && this.state.currentYouth.youth_visits.length > 0) {
            let form_data = this.state.currentYouth.youth_visits[0].forms;
            for(let i = 0; i < form_data.length; i++) {
                let form = form_data[i];
                forms_by_status[form.status].push(form);
            }
        }
        for(let i = 0; i < statuses.length; i++) {
            let status = statuses[i];
            columns.push(<YouthFormsColumn key={status} status={status} handler={this.changeFormStatusHandler} 
                                           formTypes={this.state.form_types} forms={forms_by_status[status]} />);
        }
        return columns;
    }
      
    render() {
        let columns = this.getColumns();
        // console.log(this.state.currentYouth);

        return (
            <div className="container">
                <div className="board">
                    {columns}
                </div>
            </div>
        );
    }
}