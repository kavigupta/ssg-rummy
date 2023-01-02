import React from "react";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

import Card from "./card";

const SortableCard = ({ id, selected }) => {
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({ id });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
        opacity: isDragging ? 0.5 : 1,
    };

    return (
        <li
            style={style}
            ref={setNodeRef}
            {...attributes}
            {...listeners}
        >
            <Card id={id} selected={selected}/>
        </li>
    );
};

export default SortableCard;
