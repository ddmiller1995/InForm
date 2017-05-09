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
    }

    componentWillReceiveProps(nextProps) {
        if(this.props.forms.length < nextProps.forms.length) {
            this.setState({
                open: true
            })
        }
    }

    toggleExpand() {
        this.setState({
            open: !this.state.open
        });
    }

    formatDaysRemaining(days, status) {
        if(status == "done") {
            return <span className="due-done">Done</span>;
        } else if(days < 0) {
            return <span className="due-now">{"Due " + Math.abs(days) + " days ago"}</span>;
        } else if(days < 3) {
            return <span className="due-now">{"Due in " + days + (days == 1 ? " day" : " days")}</span>;
        } else if(days < 7) {
            return <span className="due-soon">{"Due in " + days + " days"}</span>;
        } else {
            return <span className="due-later">{"Due in " + days + " days"}</span>;
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
                        {this.formatDaysRemaining(form.days_remaining, form.status)}
                    </div>
                    <div className="mdl-card__actions mdl-card--border">
                        { (form.status == "done" || form.status == "in progress") ?
                            <a className="mdl-button mdl-js-button mdl-button--icon" onClick={() => this.props.handler(form, -1)}>
                                <i className="material-icons">navigate_before</i>
                            </a>
                            : ""
                        }
                        { (form.status == "pending" || form.status == "in progress") ?
                            <a className="mdl-button mdl-js-button mdl-button--icon align-right" onClick={() => this.props.handler(form, 1)}>
                                <i className="material-icons">navigate_next</i>
                            </a>
                            : ""
                        }
                    </div>
                    
                    {/*<div className="mdl-card__menu">
                        <button className="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect mdl-button--colored">
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
                <div className={ "form-type-title" +
                    (this.props.forms.length > 0 ? " filled-form-type-title" : "" )
                }>
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