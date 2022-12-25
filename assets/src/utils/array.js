import { arrayMove as dndKitArrayMove } from "@dnd-kit/sortable";

export const arrayMove = (array, oldIndex, newIndex) => {
    array = dndKitArrayMove(array, oldIndex, newIndex);
    return array;
};
