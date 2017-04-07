import Patch from 'react-hot-loader/patch';
import React from "react";
import {AppContainer} from 'react-hot-loader';
import {render} from "react-dom";

import App from "./components/app.jsx";
import Homepage from "./components/homepage.jsx";
import Admin from "./components/admin.jsx";
import ProgressReport from "./components/progress-report.jsx";
import Youth from "./components/youth.jsx";
import YouthInfo from "./components/youth-info.jsx";
import YouthProgress from "./components/youth-progress.jsx";

import {Router, Route, IndexRoute, hashHistory} from "react-router";

"use strict";

var router = (
    <Router history={hashHistory}>
        <Route path="/" component={App}>
            <IndexRoute component={Homepage}></IndexRoute>
            <Route path="/progress" component={ProgressReport}></Route> 
            <Route path="/admin" component={Admin}></Route> 
            <Route path="/youth" component={Youth}>
                <IndexRoute component={YouthInfo}></IndexRoute>
                <Route path="/youth/progress" component={YouthProgress}></Route> 
            </Route> 
        </Route> 
    </Router>
);

render(router, document.getElementById("app"));
