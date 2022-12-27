import React from "react";


const Card = ({ id, dragOverlay }) => {
    const style = {
        cursor: dragOverlay ? "grabbing" : "grab",
    };

    const [num, card] = JSON.parse(id);

    return (
        <div id={num} style={style} className="card">
            {render_card(card)}
        </div>
    );
};

function render_card(card) {
    if (card === null) {
        return document.createTextNode("None");
    }
    const number = card[0];
    var to_suit = {
        H: "♠",
        D: "♦",
        C: "♣",
        S: "♥",
        "$": "$",
    };
    const suit = to_suit[card[1]];
    card = `${suit}${number}`;
    return card;
}


export default Card;
