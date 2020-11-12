//noinspection JSAnnotator,JSReferencingArgumentsOutsideOfFunction,JSUnresolvedVariable,ThisExpressionReferencesGlobalObjectJS
return (function() {
    function left(element) {
        return Math.round(element.getBoundingClientRect().left -
            document.body.getBoundingClientRect().left);
    }

    function top(element) {
        return Math.round(element.getBoundingClientRect().top -
                document.body.getBoundingClientRect().top);
    }

    function right(element) {
        return Math.round(element.getBoundingClientRect().right -
            document.body.getBoundingClientRect().left);
    }

    function bottom(element) {
        return Math.round(element.getBoundingClientRect().bottom -
            document.body.getBoundingClientRect().top);
    }

    var element = arguments[0];

    var _top = top(element),
        _right = right(element),
        _bottom = bottom(element),
        _left = left(element),
        _width = _right - _left,
        _height = _bottom - _top,
        _center = _left + parseInt(_width / 2),
        _middle = _top + parseInt(_height / 2);

    // the right and the bottom values need to be adjusted to be inside
    // the box.

    _right -= 1;
    _bottom -= 1;

    return [_top, _right, _bottom, _left, _center, _middle, _width, _height];
}.apply(this, arguments));
