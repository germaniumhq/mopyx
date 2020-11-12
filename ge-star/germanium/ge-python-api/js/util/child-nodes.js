//noinspection JSAnnotator,JSUnresolvedVariable,ThisExpressionReferencesGlobalObjectJS,JSReferencingArgumentsOutsideOfFunction
return (function() {
    var result = [];
    var element = arguments[0];
    var onlyElements = arguments[1];

    if (!element.childNodes) {
        return result;
    }

    for (var i = 0; i < element.childNodes.length; i++) {
        if (onlyElements && element.childNodes[i].nodeType != 1) {
            continue;
        }

        result.push(element.childNodes[i]);
    }

    return result;
}.apply(this, arguments));
