//noinspection JSAnnotator,JSReferencingArgumentsOutsideOfFunction,JSUnresolvedVariable,ThisExpressionReferencesGlobalObjectJS
return (function() {
  var rootNode = arguments[0] || document.body;
  var searchedText = arguments[1];
  var checkFunction = arguments[2] ? exact : contains; // exactMatch
  var processText = arguments[3] ? trim : noop; // trimText

  /*
   * text - returns the text of the given DOM node.
   * @param {Element} node The node to extract the text
   * @return {string}
   */
  function text(node) {
      return node.innerText || node.textContent || "";
  }

  /**
   * trim - Trims the given text.
   * @param {string} text
   * @return {string}
   */
  function trim(text) {
      return text.replace(/^\s+|\s+$/gm,'');
  }

  /**
   * noop - Keeps the text intact.
   * @param {string} text
   * @return {string}
   */
  function noop(text) {
      return text;
  }

  /**
   * contains - Checkes if the haystack string contains the needle.
   * @param {string} haystack
   * @param {string} needle
   * @return {boolean}
   */
  function contains(haystack, needle) {
      return haystack.indexOf(needle) >= 0;
  }

  /**
   * equals - Checks if the strings are equal.
   * @param {string} value1
   * @param {string} value2
   * @return {boolean}
   */
  function exact(value1, value2) {
      return value1 == value2;
  }

  // no point in searching if it's not there.
  if (!contains(text(rootNode), searchedText)) {
      return null;
  }

  /**
   * @param {Array<Element>} elements
   */
  function removeParents(elements) {
      var index2 = elements.length - 1;

      NextIndex2:
      while (index2 > 0) {
          var index1 = index2 - 1;

          while (index1 >= 0) {
            // index2 is parent of index1
            if (isParent(elements[index2], elements[index1])) {
                elements.splice(index2, 1);
                index2--;
                continue NextIndex2;
            }

            if (isParent(elements[index1], elements[index2])) {
                elements.splice(index1, 1);
                index2--; // we shift the index for the next check
            }

            index1--;
          }

          index2--;
      }

      return elements;
  }

    /**
     * Checks if the current child is a child of the
     * given parent.
     * @param parent
     * @param child
     */
  function isParent(parent, child) {
      var checkNode = child;

      while (checkNode && checkNode.parentNode != checkNode) {
          // we go first up, so isParent(node, node) returns false.
          checkNode = checkNode.parentNode;

          if (parent === checkNode) {
              return true;
          }
      }

      return false;
  }

  var processing_queue = [ rootNode ];
  var result = [];

  while (processing_queue.length) {
      var currentNode = processing_queue.splice(0, 1)[0];

      for (var i = 0; i < currentNode.children.length; i++) {
          var nodeText = processText(text(currentNode.children[i]));

          if (checkFunction(nodeText, searchedText)) {
              result.push(currentNode.children[i]);
          }

          if (contains(nodeText, searchedText)) {
              processing_queue.push(currentNode.children[i]);
          }
      }
  }

  return removeParents(result);
}.apply(this, arguments));

