import { useState } from 'react';
import React from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";

import ReactDOM from 'react-dom/client';

import { CardList } from './cards/card_list';

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
            {JSON.stringify(props.joker)}
        </span>
    );
}

function Discarded(props) {
    return (
        <span className="discarded">
            {JSON.stringify(props.discarded)}
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
    const [message, setMessage] = useState('');

    const handleChange = event => {
        setMessage(event.target.value);

        console.log('value is:', event.target.value);
    };

    function onThrow() {
        const idx = parseInt(message);
        send_command(client, { "type": "throw", "index": idx, "card": props.hand[idx] });
    }

    return (
        <div className="throw">
            <input type="text" id="throw-input" onChange={handleChange} />
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
                <CardList state={this.state.hand} setItems={fn => this.updateHand(fn)} />
                <br />
                <DrawButtons is_draw={this.is_turn("draw")} />
                <Throw is_throw={this.is_turn("throw")} hand={this.state.hand} />
            </div>
        );
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