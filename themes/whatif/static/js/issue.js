// TODO's:
// * replace <script/> with '', footnote with its number/id
// * selection / context for images? What with images selected with the footnote just before?
// * touchscreen?

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
    xhr.onreadystatechange = function(){
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
    a.addEventListener('click', function(evt){
        evt = evt || window.event;
        evt.preventDefault();
        window.open(url, name);
        return false;
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
        'rect': sel.getBoundingClientRect(),
    };
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
    return sel;
}

function isSelInsideIssueForm(sel) {
    var form = document.body.querySelector('.issue_form');
    if (form == null) {
        return false;
    }
    return form.contains(sel.startContainer) ||
        form.contains(sel.endContainer);
}

function getSelContext() {
    var sel = getSel();
    if (sel == null || isSelInsideIssueForm(sel)) {
        return null;
    }
    var context = getContextNode(sel.commonAncestorContainer,
        CONTEXT_MIN_LENGTH + sel.toString().length);
    return splitContext(sel, context);
}

// Issue form
// ==========

var TEXTAREA_ROWS = 4;
var FORM_RIGHT_AIRGAP = 30;

var lastSelContext = null;

function createIssueForm() {
    if (!isAllNeededSupported()) {
        return;
    }
    var formHTML = '<form class="issue_form">' +
        '<h4>Сообщение об ошибке</h4>' +
        '<p class="context"></p>' +
        '<label>Комментарий:</label>' +
        '<textarea rows="' + TEXTAREA_ROWS + '"></textarea>' +
        '<input type="submit" value="Отправить">'
        '</form>';
    var form = appendHTML(document.body, formHTML);

    // submit
    form.addEventListener('submit', function(evt) {
        evt = evt || window.event;
        evt.preventDefault();
        sendIssueForm(form);
        return false;
    }, false);
    form.querySelector('textarea').onkeydown = function(evt) {
        evt = evt || window.event;
        var keyCode = evt.keyCode || evt.which;
        if (isCtrlEnter(evt, keyCode)) {
            evt.stopPropagation();
            sendIssueForm(form);
            return false;
        }
    };
    // close on click outside
    document.documentElement.addEventListener('click', dropIssueForm, false);
    var content = document.body.querySelector('.content');
    content.addEventListener('click', dropIssueForm, false);
    form.addEventListener('click', function(evt) {
        evt = evt || window.event;
        evt.stopPropagation();
        return false;
    }, false);
}

function clearIssueForm(form) {
    form.querySelector('.context').innerHTML = '';
    form.querySelector('textarea').value = '';
    var responseP = form.querySelector('.response');
    if (responseP != null) {
        form.removeChild(responseP);
    }
    toogleForm(form, true);
}

function showIssueForm() {
    if (!isAllNeededSupported()) {
        return;
    }
    dropIssueForm();
    var context = getSelContext();
    if (!context) {
        return;
    }

    // all checks passed, so hold the context
    lastSelContext = context;

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

    // set initial position
    var em = getEm();
    var r = context.rect;
    var formH = form.clientHeight;
    form.style.left = (window.scrollX + r.left - 6.6*em) + 'px';
    form.style.top = (window.scrollY + r.top - formH - 1.2*em) + 'px';
    // and tweak it more left if needed
    tweakIssueFormPos();

    form.querySelector('textarea').focus();
}

// silently returns when the form is not exists or is not active
function tweakIssueFormPos() {
    var form = document.body.querySelector('.issue_form.active');
    if (form == null) {
        return;
    }
    var windowW = window.innerWidth;
    if (windowW >= 1000) {
        var formW = form.clientWidth;
        var formLeft = getPxSize(window.getComputedStyle(form).left);
        var gap = windowW - (formLeft + formW + FORM_RIGHT_AIRGAP);
        if (gap < 0) {
            form.style.left = (formLeft + gap) + 'px';
        }
    } else {
        $(this).removeAttr('style'); // TODO: ???
    }
}

function dropIssueForm() {
    var form = document.body.querySelector('.issue_form');
    form.setAttribute('class', 'issue_form'); // remove 'active'
    return false;
}

function toogleForm(form, enable) {
    [].slice.call(form.children).forEach(function(node){
        var tag = node.nodeName.toLowerCase();
        if (tag == 'textarea' || tag  == 'input') {
            node.disabled = !enable;
        }
    });
}

function sendIssueForm(form) {
    toogleForm(form, false);
    var responseP = form.querySelector('.response');
    if (responseP == null) {
        responseP = document.createElement('p');
        responseP.setAttribute('class', 'response');
        responseP.innerHTML = 'Отправка запроса…';
        form.appendChild(responseP);
    }
    var success = function(response){
        responseP.innerHTML =
            'Успех! Следить за обновлениями можно здесь: ' +
            '<a href="' + response.url + '" target="_blank">#' +
            response.num + '</a>.';
    };
    var error = function(response){
        responseP.innerHTML = 'К сожалению, что-то пошло не так. Мы очень ' +
            'извиняемся за это. Попробуйте отправить запрос еще раз — вдруг ' +
            'были проблемы со связью. Если ошибка не проходит, вы можете ' +
            'написать нам ' + '<a href="mailto:contact@chtoes.li">' +
            'на почту</a>.';
        var a = responseP.querySelector('a');
        tweakMailToNewWindow(a, 'mailto:contact@chtoes.li',
            'chtoesli_feedback');
        toogleForm(form, true);
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

// Create form when script loaded
// ==============================

createIssueForm();

// Handle window resizing
// ======================

// It's skipped too frequently events to be more responsible.
var resizeTimer_issueForm;
window.addEventListener('resize', function(){
	clearTimeout(resizeTimer_issueForm);
	resizeTimer_issueForm = setTimeout(tweakIssueFormPos, 100);
});

// Keyboard events
// ===============

var cmdKey = false;

// Old Opera maps it to Ctrl, but we handled it by KeyboardEvent.ctrlKey.
// Key codes: http://unixpapa.com/js/key.html
function isCmdKeyCode(keyCode) {
    return keyCode == 0xE0 || keyCode == 0x5B || keyCode == 0x5D;
}

// Ctrl+Enter || Cmd+Enter
function isCtrlEnter(evt, keyCode) {
    return (evt.ctrlKey || cmdKey) && (keyCode == 0x0A || keyCode == 0x0D);
}

document.onkeydown = function(evt) {
    evt = evt || window.event;
    var keyCode = evt.keyCode || evt.which;
    if (isCmdKeyCode(keyCode)) {
        cmdKey = true;
    }
    if (isCtrlEnter(evt, keyCode)) {
        showIssueForm();
    }
};

document.onkeyup = function(evt) {
    evt = evt || window.event;
    var keyCode = evt.keyCode || evt.which;
    if (isCmdKeyCode(keyCode)) {
        cmdKey = false;
    }
};
