/* Known issues / areas for enhancaments
 * =====================================
 *
 * Images
 * ------
 *
 * There are few peculiarities with images:
 *
 * An image can be selected, but it has empty textual representation. So it’s
 * not possible to select an image and report only it (the issue form will not
 * shown). When an image selected with a text near it, the image will not shown
 * in the report.
 *
 * Let the desktop layout to be on the screen. Let an image follows after a
 * paragraph which ends with a footnote. It’s seems to be not possible (Desktop
 * Firefox) to select the image w/o the start ellipsis symbol in some cases
 * (true for sun-bug/^4, false for sun-bug/^6). When the selection contains
 * such ellipsis the issue form appears on top of the non-visible footnote
 * block.
 *
 * Prettify a context
 * ------------------
 *
 * It would be nice to don’t show in a selection’s context elements not shown
 * on the screen: <script/> tags, footnotes’ bodies.
 *
 * The related enhancement is give textual representation to images (see
 * above).
 */

(function () { // module

// Utils
// =====

function cutStart(str, maxlen) {
    if (str.length > maxlen) {
        return  '<…>' + str.substring(str.length - maxlen);
    } else {
        return str;
    }
}

function cutEnd(str, maxlen) {
    if (str.length > maxlen) {
        return str.substring(0, maxlen) + '<…>';
    } else {
        return str;
    }
}

// strips 'px' from end of string and returns a float value
function getPxSize(str) {
    return parseFloat(str.match(/^(\d+(?:\.\d+)?)px$/)[1]);
}

// em size in pixels as a float value
function getEm() {
    var fontSizeStr = window.getComputedStyle(document.body).fontSize;
    return getPxSize(fontSizeStr);
}

// creates node from HTML and append it to the parent node
function appendHTML(parent, html) {
    var tmp = document.createElement('div');
    tmp.innerHTML = html;
    var elem = tmp.firstElementChild;
    parent.appendChild(elem);
    return elem;
}

function escapeTags(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/</g, '&gt;');
}

// Adopted from
// https://ponyfoo.com/articles/uncovering-the-native-dom-api#meet-xmlhttprequest
function ajaxJSON(opts) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        var COMPLETED = 4;
        if (this.readyState === COMPLETED) {
            if (this.status === 200) {
                var response = JSON.parse(this.responseText);
                opts.success(response, this);
            } else {
                opts.error(this.responseText, this);
            }
        }
    };
    xhr.open(opts.method, opts.url, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
    xhr.send(JSON.stringify(opts.json));
}

// makes email link opens in a new window
function tweakMailToNewWindow(a, url, name) {
    a.addEventListener('click', function(event) {
        event.preventDefault();
        window.open(url, name);
    }, false);
}

// slug (sort of id) of the current page
function getPageSlug() {
    var slug = window.location.pathname.replace(/(^\/+)|(\/+$)/g, '');
    var cLinkNode = document.body.querySelector('.main h1 a');
    if (cLinkNode != null) {
        var cLink = cLinkNode.getAttribute('href');
        slug = cLink.match(/^.*?\/([^\/]+)\/*$/)[1];
    }
    return slug;
}

// useful to disable all features at once when the browser is not supported
function isAllNeededSupported() {
    // false for IE < 9
    return !!window.getSelection;
}

// Selection & context
// ===================

var SELECTION_MAX_LENGTH = 256;
var CONTEXT_MIN_LENGTH = 64;
var CONTEXT_SIDE_MAX_LENGTH = 64;

function getContextNode(node, minLength) {
    function has_name(node, tag) {
        var m = node.nodeType == 1; // Node.ELEMENT_NODE
        return m && node.nodeName.toLowerCase() == tag;
    }
    function has_class(cls) {
        cls_re = new RegExp('(?:^|\\s)' + cls + '(?:$|\\s)');
        return node.className.match(cls_re);
    }
    while (node) {
        var match = (has_name(node, 'div') && has_class('page')) ||
            has_name(node, 'blockquote') ||
            has_name(node, 'p') ||
            (has_name(node, 'span') && has_class(node, 'p')) ||
            has_name(node, 'figcaption') ||
            has_name(node, 'body');
        if (match && node.textContent.length >= minLength) {
            return node;
        }
        node = node.parentNode;
    }
    return document.body;
}

function splitContext(sel, context) {
    var selStr = sel.toString();
    // get a text before selection
    var before = document.createRange();
    before.setStartBefore(context);
    before.setEnd(sel.startContainer, sel.startOffset);
    before = before.toString().replace(/^\s+/, '');
    before = cutStart(before, CONTEXT_SIDE_MAX_LENGTH);
    var m = selStr.match(/^\s/) ?
        before.match(/(?:^|\s)(\S{1,16}\s*)$/) :
        before.match(/(?:^|\s)(\S{1,16})$/);
    var before_near = m ? m[1] : '';
    var before_far = before.substring(0, before.length - before_near.length);
    // get a text after selection
    var after = document.createRange();
    after.setStart(sel.endContainer, sel.endOffset);
    after.setEndAfter(context);
    after = after.toString().replace(/\s+$/, '');
    after = cutEnd(after, CONTEXT_SIDE_MAX_LENGTH);
    m = selStr.match(/\s$/) ?
        after.match(/^(\s*\S{1,16})(?:\s|$)/) :
        after.match(/^(\S{1,16})(?:\s|$)/);
    var after_near = m ? m[1] : '';
    var after_far = after.substring(after_near.length);
    return {
        'before_far': before_far,
        'before_near': before_near,
        'sel': selStr,
        'after_near': after_near,
        'after_far': after_far,
        // for recalculating selection position after resizing
        // using .getBoundingClientRect()
        'sel_range': sel,
    };
}

function isSelInsideForm(sel) {
    var form = document.body.querySelector('.issue_form');
    if (form == null) {
        return false;
    }
    return form.contains(sel.startContainer) ||
        form.contains(sel.endContainer);
}

function getSel() {
    var selection = window.getSelection();
    if (selection.rangeCount == 0) {
        // no selection
        return null;
    }
    var sel = selection.getRangeAt(0);
    var len = sel.toString().length;
    if (len == 0 || len > SELECTION_MAX_LENGTH) {
        // the selection is zero or too big
        return null;
    }
    if (isSelInsideForm(sel)) {
        // the selection inside the issue form
        return null;
    }
    return sel;
}

function getSelContext() {
    var sel = getSel();
    if (sel == null) {
        return null;
    }
    var contextNode = getContextNode(sel.commonAncestorContainer,
        CONTEXT_MIN_LENGTH + sel.toString().length);
    return splitContext(sel, contextNode);
}

// Issue form
// ==========

var TEXTAREA_ROWS = 4;
var FORM_RIGHT_AIRGAP = 20;

var lastSelContext = null;

function createIssueForm() {
    var formHTML = '<form class="issue_form">' +
        '<h4>Сообщение об ошибке</h4>' +
        '<p class="context"></p>' +
        '<label>Комментарий:</label>' +
        '<textarea rows="' + TEXTAREA_ROWS + '"></textarea>' +
        '<input type="submit" value="Отправить">'
        '</form>';
    var form = appendHTML(document.body, formHTML);

    // submit by button or Ctrl+Enter
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        sendIssueForm(form);
    }, false);
    var textarea = form.querySelector('textarea');
    textarea.addEventListener('keydown', function(event) {
        var keyCode = event.keyCode || event.which;
        if (isCtrlEnter(event, keyCode)) {
            event.stopPropagation();
            sendIssueForm(form);
        }
    }, false);

    // close on click outside
    var content = document.body.querySelector('.content');
    document.documentElement.addEventListener('click', dropIssueForm, false);
    content.addEventListener('click', dropIssueForm, false);
    form.addEventListener('click', function(event) {
        event.stopPropagation();
    }, false);
}

function clearIssueForm(form) {
    form.querySelector('.context').innerHTML = '';
    form.querySelector('textarea').value = '';
    var responseP = form.querySelector('.response');
    if (responseP != null) {
        form.removeChild(responseP);
    }
    toogleFormFreeze(form, true);
}

function saveSelContext(context) {
    context = context || getSelContext();
    if (context) {
        lastSelContext = context;
    }
}

function showIssueForm(useSavedContext) {
    dropIssueForm();
    var context = useSavedContext ? lastSelContext : getSelContext();
    if (!context) {
        return;
    }

    saveSelContext(context);

    var form = document.body.querySelector('.issue_form');
    clearIssueForm(form);
    form.querySelector('.context').innerHTML =
        escapeTags(context.before_far) +
        '<strong>' +
        escapeTags(context.before_near) +
        '|' +
        escapeTags(context.sel) +
        '|' +
        escapeTags(context.after_near) +
        '</strong>' +
        escapeTags(context.after_far);

    form.setAttribute('class', 'issue_form active'); // add 'active'
    setIssueFormPos();
    form.querySelector('textarea').focus();
}

// silently returns when the form is not exists or is not active
// as well as when last selection is not available
function setIssueFormPos() {
    var form = document.body.querySelector('.issue_form.active');
    if (form == null || lastSelContext == null) {
        return;
    }

    var em = getEm();
    var r = lastSelContext.sel_range.getBoundingClientRect();
    var windowW = window.innerWidth;

    if (windowW >= 1000) {
        var formW = form.clientWidth;
        var desiredLeft = window.scrollX + r.left - 6.6*em;
        var gap = windowW - (desiredLeft + formW + FORM_RIGHT_AIRGAP);
        form.style.left = (desiredLeft + (gap < 0 ? gap : 0)) + 'px';
    } else {
        form.removeAttribute('style');
    }

    var formH = form.clientHeight;
    form.style.top = (scrollY + r.top - formH - 1.2*em) + 'px';
}

function dropIssueForm() {
    var form = document.body.querySelector('.issue_form');
    // prevent horizontal scrollbar from appears after window resizing
    form.removeAttribute('style');
    form.setAttribute('class', 'issue_form'); // remove 'active'
}

function toogleFormFreeze(form, enable) {
    [].slice.call(form.children).forEach(function(node) {
        var tag = node.nodeName.toLowerCase();
        if (tag == 'textarea' || tag  == 'input') {
            node.disabled = !enable;
        }
    });
}

function sendIssueForm(form) {
    toogleFormFreeze(form, false);
    var responseP = form.querySelector('.response');
    if (responseP == null) {
        responseP = document.createElement('p');
        responseP.setAttribute('class', 'response');
        responseP.innerHTML = 'Отправка запроса…';
        form.appendChild(responseP);
    }
    var success = function(response) {
        responseP.innerHTML =
            'Успех! Следить за обновлениями можно здесь: ' +
            '<a href="' + response.url + '" target="_blank">#' +
            response.num + '</a>.';
    };
    var error = function(response) {
        responseP.innerHTML = 'К сожалению, что-то пошло не так. Мы очень ' +
            'извиняемся за это. Попробуйте отправить запрос еще раз — вдруг ' +
            'были проблемы со связью. Если ошибка не проходит, вы можете ' +
            'написать нам ' + '<a href="mailto:contact@chtoes.li">' +
            'на почту</a>.';
        var a = responseP.querySelector('a');
        tweakMailToNewWindow(a, 'mailto:contact@chtoes.li',
            'chtoesli_feedback');
        toogleFormFreeze(form, true);
    };
    var textarea = form.querySelector('textarea');
    var json = {
        'comment': textarea.value,
        'slug': getPageSlug(),
    };
    Object.keys(lastSelContext).forEach(function(key) {
        if (/^(?:before_(?:far|near)|sel|after_(?:far|near))$/.test(key)) {
            json[key] = lastSelContext[key];
        }
    });
    ajaxJSON({
        'url': '/api/issue/',
        'method': 'POST',
        'json': json,
        'success': success,
        'error': error,
    });
}

// Window resizing
// ===============

var resizeTimer;

// It's skipped too frequently events to be more responsible.
function resizeHandler() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(setIssueFormPos, 100);
}

// Keyboard events
// ===============

var cmdKey = false;

// Old Opera maps it to Ctrl, but we handled it by KeyboardEvent.ctrlKey.
// Key codes: http://unixpapa.com/js/key.html
function isCmdKeyCode(keyCode) {
    return keyCode == 0xE0 || keyCode == 0x5B || keyCode == 0x5D;
}

// Ctrl+Enter || Cmd+Enter
function isCtrlEnter(event, keyCode) {
    return (event.ctrlKey || cmdKey) && (keyCode == 0x0A || keyCode == 0x0D);
}

function keyDownHandler(event) {
    var keyCode = event.keyCode || event.which;
    if (isCmdKeyCode(keyCode)) {
        cmdKey = true;
    }
    if (isCtrlEnter(event, keyCode)) {
        showIssueForm(false);
    }
}

function keyUpHandler(event) {
    var keyCode = event.keyCode || event.which;
    if (isCmdKeyCode(keyCode)) {
        cmdKey = false;
    }
}

// Touch events
// ============

var watchSelectionID;

function watchSelection() {
    saveSelContext();
    clearInterval(watchSelectionID);
    watchSelectionID = setInterval(function (){
        var context = getSelContext();
        if (context) {
            saveSelContext(context);
        } else {
            unwatchSelection();
            toogleHelperButton(false);
        }
    }, 200);
}

function unwatchSelection() {
    clearInterval(watchSelectionID);
}

function createHelperButton()
{
    var buttonHTML = '<a href="#" class="issue_helper">Ошибка?</a>';
    var button = appendHTML(document.body, buttonHTML);
    button.addEventListener('click', function(event) {
        // prevent default link behaviour
        event.preventDefault();
        // prevent closing of the form
        event.stopPropagation();
        toogleHelperButton(false);
        showIssueForm(true);
    }, false);
}

function toogleHelperButton(enable)
{
    var button = document.body.querySelector('.issue_helper');
    var cls = 'issue_helper' + (enable ? ' active' : '');
    button.setAttribute('class', cls);
    if (enable) {
        watchSelection();
    } else {
        unwatchSelection();
    }
}

function touchHandler(event)
{
    toogleHelperButton(!!getSel());
}

// Main
// ====

var mainStarted = false;

function main() {
    if (mainStarted || !isAllNeededSupported()) {
        return;
    }

    mainStarted = true;

    createIssueForm();
    window.addEventListener('resize', resizeHandler, false);
    document.addEventListener('keydown', keyDownHandler, false);
    document.addEventListener('keyup', keyUpHandler, false);

    // Test events:
    // * http://quirksmode.org/m/tests/touch.html
    // Sightings on touch events (Chrome on Android 4.4.4):
    // * touchcancel fired up when a word selected using long tap, not touchend
    // * touchmove are not generated when a selection changed
    // As result of such sightings (un)watchSelection approach is used.
    createHelperButton();
    document.addEventListener('touchstart', touchHandler, false);
    document.addEventListener('touchend', touchHandler, false);
    document.addEventListener('touchcancel', touchHandler, false);
}

// 'DOMContentLoaded' can be not fired at all (when a DOM content loaded
// before the script), so 'load' fallback is necessary.
document.addEventListener('DOMContentLoaded', main, false);
window.addEventListener('load', main, false);

}()); // module
