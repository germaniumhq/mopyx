export interface Dimensions {
    left: number
    right: number
    top: number
    bottom: number
    width: number
    height: number
    center: number
    middle: number
}

function getLeft(element: Element) {
    return Math.round(element.getBoundingClientRect().left -
        document.body.getBoundingClientRect().left);
}

function getTop(element: Element) {
    return Math.round(element.getBoundingClientRect().top -
        document.body.getBoundingClientRect().top);
}

function getRight(element: Element) {
    return Math.round(element.getBoundingClientRect().right -
        document.body.getBoundingClientRect().left);
}

function getBottom(element: Element) {
    return Math.round(element.getBoundingClientRect().bottom -
        document.body.getBoundingClientRect().top);
}

export function box(element: Element): Dimensions {
    let top = getTop(element),
        right = getRight(element),
        bottom = getBottom(element),
        left = getLeft(element),
        width = right - left,
        height = bottom - top,
        center = left + Math.round(width / 2),
        middle = top + Math.round(height / 2);

    // the right and the bottom values need to be adjusted to be inside
    // the box.
    right -= 1;
    bottom -= 1;

    return {
        top,
        right,
        bottom,
        left,
        width,
        height,
        center,
        middle,
    }
}
