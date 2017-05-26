import React from "react";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";
import {postRequest, getRequest, registerDialog, closeDialog, titleCase} from '../util.js';

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

    toggleModal(form) {
        let that = this;
        let div = this.buildDialog(form);
        // if dialog doesn't exist, append it
        if (document.getElementById("mdl-dialog") == null) {
            document.querySelector(".board").appendChild(div.firstElementChild);
        } 
        // @param1: parent container that dialog child will be added and removed from
        // @param2: index of dialog in childNodes array
        registerDialog(".board", 3);
        

        let button = document.getElementById("save-notes");
        let _this = this;
        button.addEventListener('click', function() {
            _this.postNotes(form.form_id);
        });

        
    }

    buildDialog(form) {
        let div = document.createElement("div"); 
        let modal = (
            `<dialog id="mdl-dialog" class="exit-dialog form-dialog">
                <h4>` + form.form_name + ` - ` + form.form_type + `</h4>
                <hr class="form-info-divider">
                <p><strong>Days remaining:</strong> ` + this.formatDaysRemainingText(form.days_remaining, form.status) + `</p>
                ` + (form.form_description.length > 0 ? `<p><strong>Description:</strong> ` + form.form_description + `</p>` : ``) +
                `<p><strong>Status:</strong> ` + titleCase(form.status) + 
                    (form.status == "done" && form.completed_by.full_name != null ? 
                    " - <strong>Completed by:</strong> " + form.completed_by.full_name : 
                    "") + 
                `</p>
                <p class="notes-header"><strong>Notes:</strong></p>
                <textarea name="notes" id="notes-textarea" cols="30" rows="8">` + form.notes + `</textarea>
                <div id="dialog-actions">
                    <button type="button" class="mdl-button mdl-js-button" id="save-notes">Submit</button>
                    <button type="button" class="mdl-button mdl-js-button" id="close-dialog">Close</button>
                </div>
            </dialog>`
        );

        div.innerHTML = modal;
        return div;
    }

    postNotes(formID) {
        let visitID = this.props.visitID;
        let url = "/api/visit/" + visitID + "/edit-form-note/";
        let notes = document.getElementById("notes-textarea").value;
        let data = new FormData();
        data.append("form_id", formID);
        data.append("note", notes);
        postRequest(url, data);
    }

    formatDaysRemaining(days, status) {
        if(status == "done") {
            return <span className="due-done">{this.formatDaysRemainingText(days, status)}</span>;
        } else if(days == null) {
            return <span className="no-due-date">{this.formatDaysRemainingText(days, status)}</span>;
        } else if(days < 3) {
            return <span className="due-now">{this.formatDaysRemainingText(days, status)}</span>;
        } else if(days < 7) {
            return <span className="due-soon">{this.formatDaysRemainingText(days, status)}</span>;
        } else {
            return <span className="due-later">{this.formatDaysRemainingText(days, status)}</span>;
        }
    }

    formatDaysRemainingText(days, status) {
        if(status == "done") {
            return "Done";
        } else if(days == null) {
            return "No due date";
        } else if(days < 0) {
            return "Due " + Math.abs(days) + " days ago";
        } else {
            return "Due in " + days + (days == 1 ? " day" : " days");
        }
        
    }

    compareForms(a, b) {
        let days_diff = a.days_remaining - b.days_remaining;
        if(days_diff == 0) {
            let a_name_upper = a.form_name.toUpperCase();
            let b_name_upper = b.form_name.toUpperCase();
            if(a_name_upper < b_name_upper) {
                return -1;
            } else if(a_name_upper > b_name_upper) {
                return 1;
            } else {
                return 0;
            }
        }
        return days_diff;
    }

    getFormCards() {
        let cards = [];
        let sortedForms = this.props.forms.sort(this.compareForms);
        for(let i = 0; i < sortedForms.length; i++) {
            let form = sortedForms[i];
            cards.push(
                <div key={form.form_id} className="demo-card-wide mdl-card mdl-shadow--2dp">
                    <div className="mdl-card__title" onClick={() => this.toggleModal(form)}>
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
                    <div className="mdl-card__menu">
                        <button className="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" onClick={() => this.toggleModal(form)}>
                            <i className="material-icons">info_outline</i>
                        </button>
                    </div>
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