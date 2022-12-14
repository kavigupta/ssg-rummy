import { useState } from 'react';
import React from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";

import ReactDOM from 'react-dom/client';

import { CardList } from './cards/card_list';
import Card, { JustCard } from './cards/card';

const client = new W3CWebSocket('ws://' + location.host + '/update_game_state');

const window_info = new URLSearchParams(window.location.search);

function get_user() {
    return window_info.get("user");
}


function send_command(socket, command) {
    // log('>>> ' + JSON.stringify(command), 'red');
    const update_command = {
        "command": command,
        "game_id": window_info.get("game_id"),
        "user": get_user()
    };
    socket.send(JSON.stringify(update_command));
}


function WhoseTurn(props) {
    return (
        <span className="whose-turn">
            {JSON.stringify(props.next_valid_action)}
        </span>
    );
}

function Joker(props) {
    return (
        <span className="joker">
            <JustCard dragOverlay={false} id={JSON.stringify(["joker", props.joker])} />
        </span>
    );
}

function Discarded(props) {
    return (
        <span className="discarded">
            <JustCard dragOverlay={false} id={JSON.stringify(["discarded", props.discarded])} />
        </span>
    );
}

function DrawButtons(props) {
    return (
        <div className="draw-buttons">
            <button onClick={() => send_command(client, { "type": "draw-shown" })} disabled={!props.is_draw}>Draw Shown</button>
            <button onClick={() => send_command(client, { "type": "draw-hidden" })} disabled={!props.is_draw}>Draw Hidden</button>
        </div>
    );
}

function Throw(props) {
    function onThrow() {
        const idx = props.which;
        send_command(client, { "type": "throw", "index": idx, "card": props.hand[idx] });
        props.set_which_is_selected(null);
    }

    return (
        <div className="throw">
            <button onClick={() => onThrow()} disabled={!props.is_throw}>Throw</button>
        </div>
    );
}


class MainPanel extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            next_valid_action: null,
            joker: null,
            discarded: null,
            hand: [],
            state: null,
            which_is_selected: null,
        };
    }

    componentWillMount() {
        client.onopen = () => {
            send_command(client, { "type": "view" });
            console.log('WebSocket Client Connected');
        };
        client.onmessage = (message) => {
            this.setState(JSON.parse(message.data));
        };
    }


    render() {
        return (
            <div className="main-panel">
                Whose turn: <WhoseTurn next_valid_action={this.state.next_valid_action} />
                <br />
                Joker: <Joker joker={this.state.joker} />, Discard pile: <Discarded discarded={this.state.discarded} />
                <br />
                <CardList
                    state={this.state.hand}
                    setItems={fn => this.updateHand(fn)}
                    which_is_selected={this.state.which_is_selected}
                    set_which_is_selected={(idx, new_val) => this.set_which_is_selected(idx, new_val)}
                />
                <br />
                <DrawButtons is_draw={this.is_turn("draw")} />
                <Throw
                    is_throw={this.is_turn("throw")}
                    hand={this.state.hand} which={this.state.which_is_selected}
                    set_which_is_selected={(idx, new_val) => this.set_which_is_selected(idx, new_val)}/>
            </div>
        );
    }

    set_which_is_selected(idx, new_val) {
        if (new_val) {
            this.setState({ which_is_selected: idx });
        } else {
            this.setState({ which_is_selected: null });
        }
    }

    updateHand(fn) {
        const new_state = fn(this.state.hand);
        this.setState({ hand: new_state });
        send_command(client, { "type": "update-order", "new_order": new_state })
    }

    is_turn(action) {
        return this.state.next_valid_action
            && this.state.next_valid_action[0] == get_user()
            && this.state.next_valid_action[1] === action;
    }
}

// ========================================

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<MainPanel />);

// const socket = new WebSocket();
// socket.addEventListener('message', function (event) {
//     root.setState({ display_state: event.data });
// });



// socket.onopen = () => send_command(socket, { "type": "view" });