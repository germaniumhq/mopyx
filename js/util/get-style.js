//noinspection JSAnnotator,JSUnresolvedVariable,ThisExpressionReferencesGlobalObjectJS,JSReferencingArgumentsOutsideOfFunction
return (function() {
    var element = arguments[0];
    var styleName = arguments[1];

    if (element.style && element.style[styleName]) {
        return element.style[styleName];
    } else {
        return window.getComputedStyle(element, null)[styleName];
    }
}.apply(this, arguments));
