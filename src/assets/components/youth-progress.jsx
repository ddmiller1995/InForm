import React from "react";
import {Link, IndexLink} from "react-router";
import YouthFormsColumn from "./youth-forms-column.jsx";
import "whatwg-fetch";
import {postRequest, getRequest} from '../util.js';

let form_data = [];
//statuses = ["pending", "in progress", "done"]

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            form_types: []
        };
    }

    componentDidMount() {
        let response = getRequest("/api/form-type", this, "form_types");

        // form_data.push({
        //     form_name: "form A",
        //     form_description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Maxime, perspiciatis quasi tenetur, ea sed, molestiae illo labore voluptatem fugiat delectus illum culpa dolore architecto saepe doloribus aliquid reprehenderit autem at!",
        //     default_due_date: "10",
        //     required: "false", 
        //     user_id: {
        //         username: "dakota",
        //         full_name: "dakota miller"
        //     },
        //     days_remaining: "3",
        //     status: "pending",
        //     form_type: "Intake"
        // });
        // form_data.push({
        //     form_name: "form B",
        //     form_description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. ",
        //     default_due_date: "10",
        //     required: "false", 
        //     user_id: {
        //         username: "dakota",
        //         full_name: "dakota miller"
        //     },
        //     days_remaining: "0",
        //     status: "pending",
        //     form_type: "Intake"
        // });
        // form_data.push({
        //     form_name: "form C",
        //     form_description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Maxime, perspiciatis quasi tenetur, ea sed, molestiae illo labore voluptatem fugiat delectus illum culpa dolore architecto saepe doloribus aliquid reprehenderit autem at!",
        //     default_due_date: "10",
        //     required: "false", 
        //     user_id: {
        //         username: "dakota",
        //         full_name: "dakota miller"
        //     },
        //     days_remaining: "3",
        //     status: "pending",
        //     form_type: "Psych"
        // });
        // form_data.push({
        //     form_name: "form D",
        //     form_description: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Maxime, perspiciatis quasi tenetur, ea sed, molestiae illo labore voluptatem fugiat delectus illum culpa dolore architecto saepe doloribus aliquid reprehenderit autem at!",
        //     default_due_date: "10",
        //     required: "false", 
        //     user_id: {
        //         username: "dakota",
        //         full_name: "dakota miller"
        //     },
        //     days_remaining: "0",
        //     status: "in progress",
        //     form_type: "Intake"
        // });
        // form_data.push({
        //     form_name: "form E",
        //     form_description: "Lorem ipsum",
        //     default_due_date: "10",
        //     required: "false", 
        //     user_id: {
        //         username: "dakota",
        //         full_name: "dakota miller"
        //     },
        //     days_remaining: "3",
        //     status: "done",
        //     form_type: "Outtake"
        // });
    }


    componentWillReceiveProps() {
        // try {
        //     form_data = this.props.currentYouth.youth_visits[0].forms;
        //     forceUpdate();
        // } catch(TypeError) {
        //     form_data = [];
        // }
        //forceUpdate();
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
            columns.push(<YouthFormsColumn key={status} status={status} formTypes={this.state.form_types} forms={statuses[status]} />);
        }
        return columns;
    }

      
    render() {
        let columns = this.getColumns();
        if(this.props.currentYouth.youth_visits) {
            console.log("yes");
            form_data = this.props.currentYouth.youth_visits[0].forms;
            console.log(this.props.currentYouth.youth_visits);
        }

        return (
            <div className="container">
                <div className="board">
                    {columns}
                </div>
            </div>
        );
    }
}