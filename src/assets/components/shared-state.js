import {createStore} from "redux";

"use strict";

const SET_CURRENT_YOUTH = "setCurrentYouth";
const DEFAULT_STATE = {currentYouth: {}};
const LS_KEY = "redux-store";

function reducer(state, action) {
    switch(action.type) {
        case SET_CURRENT_YOUTH:
            return Object.assign({}, state, {currentYouth: action.currentYouth});            
        default:
            return state;
    }
}

export function setCurrentYouth(youth) {
    console.log(youth);
    return {
        type: SET_CURRENT_YOUTH,
        currentYouth: {id:youth.youth_id}
    }
}

var savedState = JSON.parse(localStorage.getItem(LS_KEY));

export var store = createStore(reducer, savedState || DEFAULT_STATE);

store.subscribe(() => localStorage.setItem(LS_KEY, JSON.stringify(store.getState())));