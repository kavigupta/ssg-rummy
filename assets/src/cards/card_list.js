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


const DroppableCard = ({ id, items }) => {
    const { setNodeRef } = useDroppable({ id });

    return (
        <SortableContext id={id} items={items} strategy={rectSortingStrategy}>
            <ol className="cardlist" ref={setNodeRef}>
                {items.map((item) => (
                    <SortableCard key={item} id={item} />
                ))}
            </ol>
        </SortableContext>
    );
};


export function CardList(props) {
    var its = [...props.state.map((item, index) => JSON.stringify([index, item]))];

    const [activeId, setActiveId] = useState(null);

    const sensors = useSensors(
        useSensor(MouseSensor),
        useSensor(TouchSensor),
        useSensor(KeyboardSensor, {
            coordinateGetter: sortableKeyboardCoordinates,
        })
    );

    const handleDragStart = ({ active }) => setActiveId(active.id);

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
                />
            </div>
            <DragOverlay>{activeId ? <Card id={activeId} dragOverlay /> : null}</DragOverlay>
        </DndContext>
    );
}
