import React from "react";

import "./card.css";

export const JustCard = ({ id, dragOverlay }) => {
    return (
        <Card id={id} dragOverlay={dragOverlay} selected={false} />
    );
};

const Card = ({ id, dragOverlay, selected }) => {
    const style = {
        cursor: dragOverlay ? "grabbing" : "grab",
    };

    const [num, card] = JSON.parse(id);
    var classes = ["card", card_color(card)];

    if (selected) {
        classes.push("card_selected");
    }

    return (
        <span id={num} style={style} className={classes.join(' ')}>
            {render_card(card)}
        </span>
    );
};


function card_color(card) {
    if (card === null) {
        return "None";
    }
    const suit = card[1];
    if (suit === "H" || suit === "D") {
        return "card_red";
    }
    return "card_black";
}

function render_card(card) {
    if (card === null) {
        return "None";
    }
    const number = card[0];
    var to_suit = {
        H: "♥",
        D: "♦",
        C: "♣",
        S: "♠",
        "$": "$",
    };
    const suit = to_suit[card[1]];
    card = `${suit}${number}`;
    return card;
}


export default Card;
