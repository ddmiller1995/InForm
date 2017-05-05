import React from "react";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";
import {postRequest, getRequest} from '../util.js';

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: true
        };

        this.toggleExpand = this.toggleExpand.bind(this);
        // this.moveLeft = this.moveLeft.bind(this);
        // this.moveRight = this.moveRight.bind(this);
    }

    componentDidMount() {
    }

    toggleExpand() {
        this.setState({
            open: !this.state.open
        });
    }

    // moveLeft(form) {
    //     this.props.handler(form, -1);
        
    //     console.log("left " + form.status)
    //     let visitID = this.props.currentYouth.youth_visits[0].youth_visit_id;
    //     let data = new FormData();
    //     data.append("form_id", form.id);
    //     if(form.status == "done") {
    //         data.append("status", "in progress");
    //     } else if(form.status == "in progress") {
    //         data.append("status", "pending");
    //     } else {
    //         throw 'Error: Unexcepted status type - ' + form.status;
    //     }
    //     postRequest('/api/visit/' + visitID + 'change-form-status', data);
    // }

    // moveRight(form) {
    //     this.props.handler(form, 1);
    //     let visitID = this.props.currentYouth.youth_visits[0].youth_visit_id;
    //     let data = new FormData();
    //     data.append("form_id", form.id);
    //     if(form.status == "pending") {
    //         data.append("status", "in progress");
    //     } else if(form.status == "in progress") {
    //         data.append("status", "done");
    //     } else {
    //         throw 'Error: Unexcepted status type - ' + form.status;
    //     }
    //     postRequest('/api/visit/' + visitID + 'change-form-status', data);
    // }

    formatDaysRemaining(days) {
        if(days < 0) {
            return <span className="overdue">{"Due " + Math.abs(days) + " days ago"}</span>
        } else if(days < 3) {
            return <span className="due-soon">{"Due in " + days + (days == 1 ? " day" : " days")}</span>
        } else {
            return <span className="due-later">{"Due in " + days + "days"}</span>
        }
    }

    getFormCards() {
        let cards = [];
        for(let i = 0; i < this.props.forms.length; i++) {
            let form = this.props.forms[i];
            cards.push(
                <div key={form.form_name} className="demo-card-wide mdl-card mdl-shadow--2dp">
                    <div className="mdl-card__title">
                        <h2 className="mdl-card__title-text">{form.form_name}</h2>
                    </div>
                    <div className="mdl-card__supporting-text">
                        {this.formatDaysRemaining(form.days_remaining)}
                    </div>
                    <div className="mdl-card__actions mdl-card--border">
                        { (form.status == "done" || form.status == "in progress") ?
                            <a className="mdl-button mdl-js-button mdl-button--icon mdl-button--colored" onClick={() => this.props.handler(form, -1)}>
                                <i className="material-icons">navigate_before</i>
                            </a>
                            : ""
                        }
                        { (form.status == "pending" || form.status == "in progress") ?
                            <a className="mdl-button mdl-js-button mdl-button--icon mdl-button--colored align-right" onClick={() => this.props.handler(form, 1)}>
                                <i className="material-icons">navigate_next</i>
                            </a>
                            : ""
                        }
                    </div>
                    
                    {/*<div className="mdl-card__menu">
                        <button className="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect">
                        <i className="material-icons">share</i>
                        </button>
                    </div>*/}
                </div>
            );

        }
        return cards;

    }

    render() {
        let formCards = this.getFormCards();

        return(
            <div className="form-type">
                <div className="form-type-title">
                    {this.props.type}
                        <a className="mdl-button mdl-js-button mdl-button--icon align-right" onClick={this.toggleExpand}>
                            <i className="material-icons">{this.state.open ? "expand_more" : "expand_less"}</i>
                        </a>
                </div>
                {this.state.open ? formCards : ""}
            </div>
        );
    }
}