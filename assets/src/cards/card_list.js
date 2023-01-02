import React, { useState } from "react";
import {
    DndContext,
    DragOverlay,
    KeyboardSensor,
    MouseSensor,
    TouchSensor,
    useSensor,
    useSensors,
} from "@dnd-kit/core";
import { sortableKeyboardCoordinates } from "@dnd-kit/sortable";

import { arrayMove } from "../utils/array";

import { useDroppable } from "@dnd-kit/core";
import { rectSortingStrategy, SortableContext } from "@dnd-kit/sortable";

import SortableCard from "./sortable_card";
import Card from "./card";

import "./card_list.css";


const DroppableCard = ({ id, items, which_is_selected, update_selected }) => {
    const { setNodeRef } = useDroppable({ id });

    return (
        <SortableContext id={id} items={items} strategy={rectSortingStrategy}>
            <ol className="cardlist" ref={setNodeRef}>
                {[...Array(items.length).keys()].map((i) => (
                    <SortableCard
                        key={items[i]}
                        id={items[i]}
                        selected={which_is_selected == i}
                        update_selected={(new_selected) => update_selected(i, new_selected)} />
                ))}
            </ol>
        </SortableContext>
    );
};


export function CardList(props) {
    var its = [...props.state.map((item, index) => JSON.stringify([index, item]))];

    const [activeId, setActiveId] = useState(null);

    const [activeIndexTopLevel, setActiveIndexTopLevel] = useState(null);

    const sensors = useSensors(
        useSensor(MouseSensor),
        useSensor(TouchSensor),
        useSensor(KeyboardSensor, {
            coordinateGetter: sortableKeyboardCoordinates,
        })
    );

    const handleDragStart = ({ active }) => {
        setActiveId(active.id);
        setActiveIndexTopLevel(active.data.current.sortable.index);
        props.set_which_is_selected(active.data.current.sortable.index, true);
    }

    const handleDragCancel = () => setActiveId(null);

    const handleDragOver = ({ active, over }) => { };

    const handleDragEnd = ({ active, over }) => {
        if (!over) {
            setActiveId(null);
            return;
        }

        if (active.id !== over.id) {
            const activeIndex = active.data.current.sortable.index;
            const overIndex = over.data.current.sortable.index;

            props.setItems((items) => {
                return arrayMove(
                    items,
                    activeIndex,
                    overIndex
                );
            });
            props.set_which_is_selected(overIndex, true);
        }

        setActiveId(null);
    };

    return (
        <DndContext
            sensors={sensors}
            onDragStart={handleDragStart}
            onDragCancel={handleDragCancel}
            onDragOver={handleDragOver}
            onDragEnd={handleDragEnd}
        >
            <div className="container">
                <DroppableCard
                    id={"group1"}
                    items={its}
                    activeId={activeId}
                    key={"group1"}
                    which_is_selected={props.which_is_selected}
                    update_selected={props.set_which_is_selected}
                />
            </div>
            <DragOverlay>{activeId ? <Card id={activeId} dragOverlay selected={activeIndexTopLevel == props.which_is_selected} /> : null}</DragOverlay>
        </DndContext>
    );
}
