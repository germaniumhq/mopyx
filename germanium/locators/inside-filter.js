//noinspection JSAnnotator,JSUnresolvedVariable,JSReferencingArgumentsOutsideOfFunction,ThisExpressionReferencesGlobalObjectJS
return (function() {
    var insideElements = [],
        containingElements = [],
        outsideElements = [],
        groupCount,
        containingAllElements = [],
        withoutChildren,
        elements = [],
        i, j, k,
        count,
        args;

    args = [];
    for (i = 0; i < arguments.length; i++) {
        args.push(arguments[i]);
    }

    function readElements(targetArray, itemsPerElement) {
        count = args.shift();
        itemsPerElement = itemsPerElement ? itemsPerElement : 1;
        while (count--) {
            targetArray.push(args.shift());
            if (itemsPerElement == 2) {
                var groups = args.shift().split(","),
                    groupIndexes = [];

                for (var k = 0; k < groups.length; k++) {
                    groupIndexes.push(parseInt(groups[k]));
                }

                targetArray.push(groupIndexes);
            }
        }
    }

    withoutChildren = args.shift();
    readElements(insideElements);
    readElements(containingElements);
    readElements(outsideElements);
    groupCount = args.shift(); // the number of groups, aka selectors passed to contains_all
    readElements(containingAllElements, 2);
    readElements(elements);

    function isInside(parentNode, childNode) {
        if (!childNode || !parentNode) {
            return false;
        }

        while (childNode) {
            if (childNode == parentNode) {
                return true;
            }

            childNode = childNode.parentNode;
        }

        return false;
    }

    if (withoutChildren) {
        for (i = elements.length - 1; i >= 0; i--) {
            if (elements[i].childNodes &&
                elements[i].childNodes.length) {

                elements.splice(i, 1);
            }
        }
    }

    if (insideElements.length) {
        nextI:
        for (i = elements.length - 1; i >= 0; i--) {
            for (j = 0; j < insideElements.length; j++) {
                if (isInside(insideElements[j], elements[i])) {
                    continue nextI;
                }
            }

            elements.splice(i, 1);
        }
    }

    if (containingElements.length) {
        nextI:
        for (i = elements.length - 1; i >= 0; i--) {
            for (j = 0; j < containingElements.length; j++) {
                if (isInside(elements[i], containingElements[j])) {
                    continue nextI;
                }
            }

            elements.splice(i, 1);
        }
    }

    if (containingAllElements.length) {
        nextI:
        for (i = elements.length - 1; i >= 0; i--) {
            var missingGroups = {};
            for (k = 0; k < groupCount; k++) {
                missingGroups[k] = true;
            }

            for (j = 0; j < containingAllElements.length; j+=2) {
                // if we already match the group, we can skip the
                // elements in the same group.
                if (!missingGroups[containingAllElements[j + 1]]) {
                    continue;
                }

                // if the element contains an element, mark all the
                // groups as matched.
                if (isInside(elements[i], containingAllElements[j])) {
                    for (k = 0; k < containingAllElements[j + 1].length; k++) {
                        delete missingGroups[containingAllElements[j + 1][k]];
                    }
                }
            }

            // if is there any group missing, then our element is out.
            for (k = 0; k < groupCount; k++) {
                if (missingGroups[k]) {
                    elements.splice(i, 1);
                    continue nextI;
                }
            }
        }
    }

    nextElement:
    for (var i = elements.length - 1; i >= 0; i--) {
        var element = elements[i];
        for (var j = 0; j < outsideElements.length; j++) {
            var outsideElement = outsideElements[j];
            if (isInside(outsideElement, element)) {
                elements.splice(i, 1);
                continue nextElement;
            }
        }
    }

    return elements;
}.apply(this, arguments));

