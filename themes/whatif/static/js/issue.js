// TODO's:
// * Ctrl+Enter to send the form and leave it on the screen
// * replace <script/> with '', footnote with its number/id
// * create form ahead and make it visible when needed with animation
// * readable template for the form
// * selection / context for images? What with images selected with the footnote just before?
// * touchscreen?

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

function cutStart(str, maxlen) {
    if (str.length > maxlen) {
        return  '<...>' + str.substring(str.length - maxlen);
    } else {
        return str;
    }
}

function cutEnd(str, maxlen) {
    if (str.length > maxlen) {
        return str.substring(0, maxlen) + '<...>';
    } else {
        return str;
    }
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
    if (!window.getSelection) {
        // IE < 9
        return null;
    }
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

function getSelContext() {
    var sel = getSel();
    if (sel == null) {
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

function getPxSize(str) {
    return parseFloat(str.match(/^(\d+(?:\.\d+)?)px$/)[1]);
}

function getEm() {
    var fontSizeStr = window.getComputedStyle(document.body).fontSize;
    return getPxSize(fontSizeStr);
}

function showIssueForm() {
    dropIssueForm(null);
    var context = getSelContext();
    if (!context) {
        return;
    }

    // all checks passed, so hold the context
    lastSelContext = context;

    form = document.createElement('form');
    form.setAttribute('class', 'issue_form');
    title = document.createElement('h4');
    title.innerHTML = 'Сообщение об ошибке';
    form.appendChild(title);
    contextP = document.createElement('p');
    contextP.innerHTML =
        context.before_far +
        '<strong>' + context.before_near +
        '|' + context.sel + '|' +
        context.after_near + '</strong>' +
        context.after_far;
    form.appendChild(contextP)
    document.body.appendChild(form);
    label = document.createElement('label');
    label.innerHTML = 'Комментарий:';
    form.appendChild(label);
    textarea = document.createElement('textarea');
    textarea.setAttribute('rows', TEXTAREA_ROWS);
    form.appendChild(textarea);
    submit = document.createElement('input');
    submit.setAttribute('type', 'submit');
    submit.setAttribute('value', 'Отправить');
    form.appendChild(submit);
    form.addEventListener('submit', sendIssueForm, false);

    // close on click outside
    stopPropagation = function(evt) {
        evt = evt || window.event;
        evt.stopPropagation();
        return false;
    };
    document.documentElement.addEventListener('click', dropIssueForm, false);
    var content = document.body.querySelector('.content');
    content.addEventListener('click', dropIssueForm, false);
    form.addEventListener('click', stopPropagation, false);

    // set initial position
    var em = getEm();
    var r = context.rect;
    var formH = form.clientHeight;
    form.style.left = (window.scrollX + r.left - 6.6*em) + 'px';
    form.style.top = (window.scrollY + r.top - formH - 1.2*em) + 'px';
    tweakIssueFormPos();
}

function tweakIssueFormPos() {
    var form = document.body.querySelector('.issue_form');
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
    var childs = document.body.querySelectorAll('.issue_form');
    Array.prototype.forEach.call(childs, function(node){
        document.body.removeChild(node);
    });
    return false;
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

function toogleForm(form, enable) {
    [].slice.call(form.children).forEach(function(node){
        var tag = node.nodeName.toLowerCase();
        if (tag == 'textarea' || tag  == 'input') {
            node.disabled = !enable;
        }
    });
}

function tweakMailToNewWindow(a, url, name) {
    a.addEventListener('click', function(evt){
        evt = evt || window.event;
        evt.preventDefault();
        window.open(url, name);
        return false;
    }, false);
}

function getSlug() {
    var slug = window.location.pathname.replace(/(^\/+)|(\/+$)/g, '');
    var cLinkNode = document.body.querySelector('.main h1 a');
    if (cLinkNode != null) {
        var cLink = cLinkNode.getAttribute('href');
        slug = cLink.match(/^.*?\/([^\/]+)\/*$/)[1];
    }
    return slug;
}

function sendIssueForm(evt) {
    evt = evt || window.event;
    evt.preventDefault();
    var form = this;
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
        'slug': getSlug(),
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
    return false;
}

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

document.onkeydown = function(evt) {
    evt = evt || window.event;
    var keyCode = evt.keyCode || evt.which;
    if (isCmdKeyCode(keyCode)) {
        cmdKey = true;
    }
    // Ctrl+Enter || Cmd+Enter
    if ((evt.ctrlKey || cmdKey) && keyCode == 0x0D) {
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
