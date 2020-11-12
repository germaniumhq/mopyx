//noinspection JSAnnotator,JSUnresolvedVariable,JSReferencingArgumentsOutsideOfFunction,ThisExpressionReferencesGlobalObjectJS
return (function() {
    var i,
        result = [];

    function left(element) {
        if (!element) {
            throw new Error('no element in left')
        }
        return Math.round(element.getBoundingClientRect().left) -
            Math.round(document.body ? document.body.getBoundingClientRect().left: 0);
    }

    function top(element) {
        if (!element) {
            throw new Error('no element in top')
        }
        return Math.round(element.getBoundingClientRect().top) -
            Math.round(document.body ? document.body.getBoundingClientRect().top : 0);
    }

    function right(element) {
        if (!element) {
            throw new Error('no element in right')
        }
        return Math.round(element.getBoundingClientRect().right) -
            Math.round(document.body ? document.body.getBoundingClientRect().left : 0) - 1;
    }

    function bottom(element) {
        if (!element) {
            throw new Error('no element in bottom')
        }
        return Math.round(element.getBoundingClientRect().bottom) -
            Math.round(document.body ? document.body.getBoundingClientRect().top : 0) - 1;
    }


    var getCssProperty = !(window.attachEvent && !window.addEventListener) ?
        function (element, property) { // anything else
            return getComputedStyle(element)[property];
        } :
        function (element, property) { // IE8
            return element.currentStyle[property];
        };

    /**
     * Check if the given element is displayed on the screen or not.
     *
     * @param element
     */
    function isDisplayed(element) {
        if (!element) {
            return false;
        }

        var l = left(element),
            r = right(element),
            t = top(element),
            b = bottom(element);

        if (element.tagName == "BODY") {
            return true;
        }

        if (b < 0) { // above the current view
            return false;
        }

        if (r < 0) { // left of current screen
            return false;
        }

        if (b - t == 0 || r - l == 0) { // 0px size
            return false;
        }

        if (getCssProperty(element, "display") == "none") {
            return false;
        }

        if (getCssProperty(element, "visibility") == "hidden") {
            return false;
        }

        return true;
    }

    for (i = 0; i < arguments.length; i++) {
        if (isDisplayed(arguments[i])) {
            result.push( arguments[i] );
        }
    }

    return result;
}.apply(this, arguments));
