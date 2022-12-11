const window_info = new URLSearchParams(window.location.search);

const log = (text, color) => {
    document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
};

function updateHand(cards) {
    var x = "";
    for (var i = 0; i < cards.length; i++) {
        x += (i + 1) + ". " + JSON.stringify(cards[i]);
        x += "<br>";
    }
    document.getElementById('hand').innerHTML = x;
}

function update_view(ev) {
    const data = JSON.parse(ev.data);
    log('<<< ' + JSON.stringify(data["state"]), 'blue');
    updateHand(data["hand"]);
}

function send_command(socket, command) {
    const update_command = {
        "command": command,
        "game_id": window_info.get("game_id"),
        "user": window_info.get("user")
    };
    socket.send(JSON.stringify(update_command));
}

const socket = new WebSocket('ws://' + location.host + '/update_game_state');
socket.addEventListener('message', update_view);
document.getElementById('form').onsubmit = ev => {
    ev.preventDefault();
    const textField = document.getElementById('text');
    log('>>> ' + textField.value, 'red');
    send_command(socket, textField.value);
    textField.value = '';
};

socket.onopen = () => send_command(socket, "view");