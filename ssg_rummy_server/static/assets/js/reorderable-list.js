/* Made with love by @fitri
 This is a component of my ReactJS project
https://www.codehim.com/vanilla-javascript/javascript-drag-and-drop-reorder-list

Modified to include a hook.

*/

handles = {}

function enableDragSort(listClass, onDragEnd) {
    const sortableLists = document.getElementsByClassName(listClass);
    Array.prototype.map.call(sortableLists, (list) => { enableDragList(listClass, list) });
    handles[listClass] = onDragEnd;
}

function enableDragList(listClass, list) {
    Array.prototype.map.call(list.children, (item) => {
        enableDragItem(item);
        item.setAttribute("parent-class", listClass);
    });
}

function enableDragItem(item) {
    item.setAttribute('draggable', true)
    item.ondrag = handleDrag;
    item.ondragend = handleDrop;
}

function handleDrag(item) {
    const selectedItem = item.target,
        list = selectedItem.parentNode,
        x = event.clientX,
        y = event.clientY;

    selectedItem.classList.add('drag-sort-active');
    let swapItem = document.elementFromPoint(x, y) === null ? selectedItem : document.elementFromPoint(x, y);

    if (list === swapItem.parentNode) {
        swapItem = swapItem !== selectedItem.nextSibling ? swapItem : swapItem.nextSibling;
        list.insertBefore(selectedItem, swapItem);
    }
}

function handleDrop(item) {
    item.target.classList.remove('drag-sort-active');
    const parent_hook = item.target.getAttribute("parent-class");
    handles[parent_hook]();
}