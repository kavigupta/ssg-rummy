const window_info = new URLSearchParams(window.location.search);

const log = (text, color) => {
    document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
};

var last_cards = [];

function updateHand(cards) {
    if (JSON.stringify([...cards].sort()) === JSON.stringify([...last_cards].sort())) {
        return;
    }
    const hand_display = document.getElementById('hand');
    hand_display.innerHTML = "";
    var x = "";
    for (var i = 0; i < cards.length; i++) {
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(JSON.stringify(cards[i])));
        li.setAttribute("order-in-array", i);
        hand_display.appendChild(li);
    }
    enableDragSort('drag-sort-enable', on_hand_order_updated);
    last_cards = cards;
}

function update_view(ev) {
    const data = JSON.parse(ev.data);
    log('<<< ' + JSON.stringify(data["state"]), 'blue');
    updateHand(data["hand"]);
}

function send_command(socket, command) {
    log('>>> ' + JSON.stringify(command), 'red');
    const update_command = {
        "command": command,
        "game_id": window_info.get("game_id"),
        "user": window_info.get("user")
    };
    socket.send(JSON.stringify(update_command));
}

const socket = new WebSocket('ws://' + location.host + '/update_game_state');
socket.addEventListener('message', update_view);
document.getElementById('throw').onsubmit = ev => {
    ev.preventDefault();
    const textField = document.getElementById('to-throw');
    send_command(socket, { "type": "throw", "to-throw": textField.value });
    textField.value = '';
};

document.getElementById('draw-shown').onclick = ev => {
    send_command(socket, { "type": "draw-shown" });
};

document.getElementById('draw-hidden').onclick = ev => {
    send_command(socket, { "type": "draw-hidden" });
};


function on_hand_order_updated() {
    const new_cards = [...document.getElementById('hand').children]
        .map(c => last_cards[c.getAttribute("order-in-array")]);
    send_command(socket, { "type": "update-order", "new-order": new_cards })
}

socket.onopen = () => send_command(socket, { "type": "view" });