(function() {

var lastCheckedTime = -1,
    AJAX_OPERATION_TIMEOUT = 0;

if (typeof window.AJAX_OPERATION_TIMEOUT != "undefined") {
    AJAX_OPERATION_TIMEOUT = window.AJAX_OPERATION_TIMEOUT;
}

XMLHttpRequest.interceptorsBefore.push(function() {
    lastCheckedTime = -1;
});

XMLHttpRequest.interceptorsAfter.push(function() {
    lastCheckedTime = -1;
});

XMLHttpRequest.isAjaxRunning = function() {
    if (AJAX_OPERATION_TIMEOUT == 0) {
        return XMLHttpRequest.runningCalls != 0;
    }

    if (lastCheckedTime < 0) {
        lastCheckedTime = new Date().getTime();
        return true;
    }

    var currentTime = new Date().getTime();

    if (currentTime - lastCheckedTime > AJAX_OPERATION_TIMEOUT && XMLHttpRequest.runningCalls == 0) {
        window.AJAX_OPERATION_TIMEOUT = 0;
        lastCheckedTime = -1;
        return false;
    }

    return true;
};

})();
