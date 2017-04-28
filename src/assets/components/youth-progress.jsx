import React from "react";
import {Link, IndexLink} from "react-router";
import YouthFormsColumn from "./youth-forms-column.jsx";
import "whatwg-fetch";

let form_data = [];
//statuses = ["pending", "in progress", "done"]

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
        console.log(this.props.currentYouth);
        form_data.push({
            form_name: "form A",
            status: "pending",
            form_type: "intake"
        });
        form_data.push({
            form_name: "form B",
            status: "pending",
            form_type: "intake"
        });
        form_data.push({
            form_name: "form C",
            status: "pending",
            form_type: "intake"
        });
        form_data.push({
            form_name: "form D",
            status: "in progress",
            form_type: "intake"
        });
        form_data.push({
            form_name: "form E",
            status: "done",
            form_type: "intake"
        });
    }

    getColumns() {
        let columns = [];
        let statuses = {};
        for(let i = 0; i < form_data.length; i++) {
            let form = form_data[i];
            if(!(form.status in statuses)) {
                statuses[form.status] = []
            }
            statuses[form.status].push(form);
        }
        for(status in statuses) {
            columns.push(<YouthFormsColumn key={status} forms={statuses[status]} />);
        }
        return columns;
    }

      
    render() {
        let columns = this.getColumns();

        return (
            <div className="container">
                <div className="kanban-board">
                    {columns}
                </div>
            </div>
        );
    }
}