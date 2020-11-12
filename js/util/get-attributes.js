//noinspection JSAnnotator,JSUnresolvedVariable,ThisExpressionReferencesGlobalObjectJS,JSReferencingArgumentsOutsideOfFunction
return (function() {
    var attributes = arguments[0].attributes;
    var result = {};

    for (var i = 0; i < attributes.length; i++) {
        if (attributes[i].specified) {
            result[attributes[i].name] = attributes[i].value;
        }
    }

    return result;
}.apply(this, arguments));

