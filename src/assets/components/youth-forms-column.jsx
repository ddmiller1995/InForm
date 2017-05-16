import React from "react";
import {Link, IndexLink} from "react-router";
import YouthFormsType from "./youth-forms-type.jsx";
import {titleCase} from '../util.js';
import "whatwg-fetch";


export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};

        this.changeFormStatusHandler = this.changeFormStatusHandler.bind(this);
    }

    componentDidMount() {
    }

    changeFormStatusHandler(form, direction) {
        this.props.handler(form, direction);
    }

    getFormTypes() {
        let forms_by_type = {}
        this.props.formTypes.forEach(function(type) {
            forms_by_type[type.form_type_name] = [];
        });
        if(this.props.formTypes.length > 0 && this.props.forms.length > 0) {
            for(let i = 0; i < this.props.forms.length; i++) {
                let form = this.props.forms[i];
                forms_by_type[form.form_type].push(form);
            }
        }

        let type_components = [];
        for(let i = 0; i < this.props.formTypes.length; i++) {
            let type_id = this.props.formTypes[i].id;
            let type = this.props.formTypes[i].form_type_name;
            type_components[type_id] = <YouthFormsType key={type} type={type} handler={this.changeFormStatusHandler} forms={forms_by_type[type]} />
        }

        return type_components;
    }
      
    render() {
        let types = this.getFormTypes();

        return (
            <div className="col">
                <header className="mdl-layout__header is-casting-shadow">
                    <div className="mdl-layout__header-row">
                        <span className="mdl-layout-title">{titleCase(this.props.status)}</span>
                    </div>
                </header>
                {types != null ? types : <span className="no-forms-message">No Forms Found</span> }
            </div>
        );
    }
}