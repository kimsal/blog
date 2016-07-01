/**
 * translate a string
 * @param app the id of the app for which to translate the string
 * @param text the string to translate
 * @return string
 */
function t(app, text) {
    if (!(app in t.cache)) {
        $.ajax(G.filePath('core', 'ajax', 'translations.php'), {
            async: false, //todo a proper sollution for this without sync ajax calls
            data: {'app': app},
            type: 'POST',
            success: function(jsondata) {
                t.cache[app] = jsondata.data;
            },
        });

        // Bad answer ...
        if (!(app in t.cache)) {
            t.cache[app] = [];
        }
    }
    if (typeof(t.cache[app][text]) !== 'undefined') {
        return t.cache[app][text];
    }
    else {
        return text;
    }
}
t.cache = {};



/*
 * Sanitizes a HTML string
 * @param string
 * @return Sanitized string
 */
function escapeHTML(s) {
    return s.toString().split('&').join('&amp;').split('<').join('&lt;').split('"').join('&quot;');
}

G = {
    webroot: 'http://localhost/galcsy/',
    appswebroot: 'http://localhost/galcsy/',
    currentUser: (typeof oc_current_user !== 'undefined') ? oc_current_user : false,
    coreApps: ['', 'admin', 'log', 'search', 'user', 'core', '3rdparty', 'box', 'message', ],
    /**
     * get an absolute url to a file in an appen
     * @param app the id of the app the file belongs to
     * @param file the file path relative to the app folder
     * @return string
     */
    linkTo: function(app, file) {
        return G.filePath(app, '', file);
    },
    /**
     * get the absolute url for a file in an app
     */
    webPath: function(app, file) {
        var ele = app.toUpperCase() + '_WEB_PATH';
        var link = $('#' + ele).val() + file;
        return link;
        //app = box

    },
    /**
     * get the absolute url for a file in an app
     * @param app the id of the app
     * @param type the type of the file to link to (e.g. css,img,ajax.template)
     * @param file the filename
     * @return string
     */
    filePath: function(app, type, file) {
        var isCore = G.coreApps.indexOf(app) != -1;
        var link = G.webroot;
        if ((file.substring(file.length - 3) == 'php' || file.substring(file.length - 3) == 'css') && !isCore) {
            link += '/?app=' + app;
            if (file != 'index.php') {
                link += '&getfile=';
                if (type) {
                    link += encodeURI(type + '/');
                }
                link += file;
            }
        } else if (file.substring(file.length - 3) != 'php' && !isCore) {
            link = G.appswebroot;
            link += '/';
            link += 'apps/';
            link += app + '/';
            if (type) {
                link += type + '/';
            }
            link += file;
        } else {
            link += '/';
            if (!isCore) {
                link += 'apps/';
            }
            if (app != '') {
                app += '/';
                link += app;
            }
            if (type) {
                link += type + '/';
            }
            link += file;
        }
        return link;
    },
    /**
     * get the absolute path to an image file
     * @param app the app id to which the image belongs
     * @param file the name of the image file
     * @return string
     * 
     * if no extension is given for the image, it will automatically decide between .png and .svg based on what the browser supports
     */
    imagePath: function(app, file) {
        if (file.indexOf('.') == -1) {//if no extension is given, use png or svg depending on browser support
            file += (SVGSupport()) ? '.svg' : '.png';
        }
        return G.filePath(app, 'img', file);
    },
    /**
     * load a script for the server and load it
     * @param app the app id to which the script belongs
     * @param script the filename of the script
     * @param ready event handeler to be called when the script is loaded
     * 
     * if the script is already loaded, the event handeler will be called directly
     */
    addScript: function(app, script, ready) {
        var path = G.filePath(app, 'js', script + '.js');
        if (G.addScript.loaded.indexOf(path) == -1) {
            G.addScript.loaded.push(path);
            if (ready) {
                $.getScript(path, ready);
            } else {
                $.getScript(path);
            }
        } else {
            if (ready) {
                ready();
            }
        }
    },
    /**
     * load a css file and load it
     * @param app the app id to which the css style belongs
     * @param style the filename of the css file
     */
    addStyle: function(app, style) {
        var path = G.filePath(app, 'css', style + '.css');
        if (G.addStyle.loaded.indexOf(path) == -1) {
            G.addStyle.loaded.push(path);
            var style = $('<link rel="stylesheet" type="text/css" href="' + path + '"/>');
            $('head').append(style);
        }
    },
    /**
     * do a search query and display the results
     * @param query the search query
     */
    search: function(query) {
        if (query) {
            G.addStyle('search', 'results');
            $.getJSON(G.filePath('search', 'ajax', 'search.php') + '?query=' + encodeURIComponent(query), function(results) {
                G.search.lastResults = results;
                G.search.showResults(results);
            });
        }
    },
    dialogs: '',
    mtime2date: function(mtime) {
        mtime = parseInt(mtime);
        var date = new Date(1000 * mtime);
        var ret = date.getDate() + '.' + (date.getMonth() + 1) + '.' + date.getFullYear() + ', ' + date.getHours() + ':' + date.getMinutes();
        return ret;
    }
};
G.search.customResults = {};
G.search.currentResult = -1;
G.search.lastQuery = '';
G.search.lastResults = {};
G.addStyle.loaded = [];
G.addScript.loaded = [];

if (typeof localStorage != 'undefined' && localStorage != null) {
    //user and instance awere localstorage
    G.localStorage = {
        namespace: 'oc_' + G.currentUser + '_' + G.webroot + '_',
        hasItem: function(name) {
            return G.localStorage.getItem(name) != null;
        },
        setItem: function(name, item) {
            return localStorage.setItem(G.localStorage.namespace + name, JSON.stringify(item));
        },
        getItem: function(name) {
            if (localStorage.getItem(G.localStorage.namespace + name) == null) {
                return null;
            }
            return JSON.parse(localStorage.getItem(G.localStorage.namespace + name));
        }
    };
} else {
    //dummy localstorage
    G.localStorage = {
        hasItem: function(name) {
            return false;
        },
        setItem: function(name, item) {
            return false;
        },
        getItem: function(name) {
            return null;
        }
    };
}

/**
 * implement Array.filter for browsers without native support
 */
if (!Array.prototype.filter) {
    Array.prototype.filter = function(fun /*, thisp*/) {
        var len = this.length >>> 0;
        if (typeof fun != "function")
            throw new TypeError();

        var res = [];
        var thisp = arguments[1];
        for (var i = 0; i < len; i++) {
            if (i in this) {
                var val = this[i]; // in case fun mutates this
                if (fun.call(thisp, val, i, this))
                    res.push(val);
            }
        }
        return res;
    };
}
/**
 * implement Array.indexOf for browsers without native support
 */
if (!Array.prototype.indexOf) {
    Array.prototype.indexOf = function(elt /*, from*/)
    {
        var len = this.length;

        var from = Number(arguments[1]) || 0;
        from = (from < 0)
                ? Math.ceil(from)
                : Math.floor(from);
        if (from < 0)
            from += len;

        for (; from < len; from++)
        {
            if (from in this &&
                    this[from] === elt)
                return from;
        }
        return -1;
    };
}

/**
 * check if the browser support svg images
 */
function SVGSupport() {
    return SVGSupport.checkMimeType.correct && !!document.createElementNS && !!document.createElementNS('http://www.w3.org/2000/svg', "svg").createSVGRect;
}
SVGSupport.checkMimeType = function() {
    $.ajax({
        url: G.imagePath('core', 'breadcrumb.svg'),
        success: function(data, text, xhr) {
            var headerParts = xhr.getAllResponseHeaders().split("\n");
            var headers = {};
            $.each(headerParts, function(i, text) {
                if (text) {
                    var parts = text.split(':', 2);
                    if (parts.length == 2) {
                        var value = parts[1].trim();
                        if (value[0] == '"') {
                            value = value.substr(1, value.length - 2);
                        }
                        headers[parts[0]] = value;
                    }
                }
            });
            if (headers["Content-Type"] != 'image/svg+xml') {
                replaceSVG();
                SVGSupport.checkMimeType.correct = false;
            }
        }
    });
};
SVGSupport.checkMimeType.correct = true;

//replace all svg images with png for browser compatibility
function replaceSVG() {
    $('img.svg').each(function(index, element) {
        element = $(element);
        var src = element.attr('src');
        element.attr('src', src.substr(0, src.length - 3) + 'png');
    });
    $('.svg').each(function(index, element) {
        element = $(element);
        var background = element.css('background-image');
        if (background) {
            var i = background.lastIndexOf('.svg');
            if (i >= 0) {
                background = background.substr(0, i) + '.png' + background.substr(i + 4);
                element.css('background-image', background);
            }
        }
        element.find('*').each(function(index, element) {
            element = $(element);
            var background = element.css('background-image');
            if (background) {
                var i = background.lastIndexOf('.svg');
                if (i >= 0) {
                    background = background.substr(0, i) + '.png' + background.substr(i + 4);
                    element.css('background-image', background);
                }
            }
        });
    });
}

/**
 * prototypal inharitence functions
 * 
 * usage:
 * MySubObject=object(MyObject)
 */
function object(o) {
    function F() {
    }
    F.prototype = o;
    return new F();
}


/**
 * Fills height of window. (more precise than height: 100%;)
 */
function fillHeight(selector) {
    if (selector.length == 0) {
        return;
    }
    var height = parseFloat($(window).height()) - (selector.offset().top + 5);
    selector.css('height', height + 'px');
    if (selector.outerHeight() > selector.height())
        selector.css('height', height - (selector.outerHeight() - selector.height()) + 'px');
}

/**
 * Fills height and width of window. (more precise than height: 100%; or width: 100%;)
 */
function fillWindow(selector) {
    if (selector.length == 0) {
        return;
    }
    fillHeight(selector);
    var width = parseFloat($(window).width()) - selector.offset().left;
    selector.css('width', width + 'px');
    if (selector.outerWidth() > selector.width())
        selector.css('width', width - (selector.outerWidth() - selector.width()) + 'px');
}

/**
 * Filter Jquery selector by attribute value
 **/
$.fn.filterAttr = function(attr_name, attr_value) {
    return this.filter(function() {
        return $(this).attr(attr_name) === attr_value;
    });
};

function humanFileSize(size) {
    humanList = ['B', 'kB', 'MB', 'GB', 'TB'];
    // Calculate Log with base 1024: size = 1024 ** order
    order = Math.floor(Math.log(size) / Math.log(1024));
    // Stay in range of the byte sizes that are defined
    order = Math.min(humanList.length - 1, order);
    readableFormat = humanList[order];
    relativeSize = (size / Math.pow(1024, order)).toFixed(1);
    if (relativeSize.substr(relativeSize.length - 2, 2) == '.0') {
        relativeSize = relativeSize.substr(0, relativeSize.length - 2);
    }
    return relativeSize + ' ' + readableFormat;
}

function simpleFileSize(bytes) {
    mbytes = Math.round(bytes / (1024 * 1024 / 10)) / 10;
    if (bytes == 0) {
        return '0';
    }
    else if (mbytes < 0.1) {
        return '< 0.1';
    }
    else if (mbytes > 1000) {
        return '> 1000';
    }
    else {
        return mbytes.toFixed(1);
    }
}

function formatDate(date) {
    if (typeof date == 'number') {
        date = new Date(date);
    }
    var monthNames = [t('files', 'January'), t('files', 'February'), t('files', 'March'), t('files', 'April'), t('files', 'May'), t('files', 'June'),
        t('files', 'July'), t('files', 'August'), t('files', 'September'), t('files', 'October'), t('files', 'November'), t('files', 'December')];
    return monthNames[date.getMonth()] + ' ' + date.getDate() + ', ' + date.getFullYear() + ', ' + ((date.getHours() < 10) ? '0' : '') + date.getHours() + ':' + ((date.getMinutes() < 10) ? '0' : '') + date.getMinutes();
}

/*
 Notify to user when something happen
 */
function notify(title, msg, type)
{
    type = getNotifyClass(type);
    //$('#notify-area').notify({
    //    type: type,
    //    closable: false,
    //    message: {html: msg}
    //}).show(); // for the ones that aren't closable and don't fade out there is a .hide() function.
    ////calculate center
    //x = $('#notify').position();
    //left = ($(window).width() - $('#notify').width()) / 2;
    //$('#notify').css({'left': left});

    $.notify({
        // options
        icon: 'glyphicon glyphicon-warning-sign',
        title: title,
        message: msg,
        url: '#',
        target: 'normal'
    },{
        // settings
        element: 'body',
        position: null,
        type: "info",
        allow_dismiss: true,
        newest_on_top: false,
        showProgressbar: false,
        placement: {
            from: "top",
            align: "right"
        },
        offset: 20,
        spacing: 10,
        z_index: 1031,
        delay: 5000,
        timer: 1000,
        url_target: '_blank',
        mouse_over: null,
        animate: {
            enter: 'animated fadeInDown',
            exit: 'animated fadeOutUp'
        },
        onShow: null,
        onShown: null,
        onClose: null,
        onClosed: null,
        icon_type: 'class',
        template: '<div data-notify="container" class="col-xs-11 col-sm-5 alert alert-{0}" role="alert">' +
        '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
        '<span data-notify="icon"></span> ' +
        '<span data-notify="title">{1}</span> ' +
        '<span data-notify="message">{2}</span>' +
        '<div class="progress" data-notify="progressbar">' +
        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
        '</div>' +
        '<a href="{3}" target="{4}" data-notify="url"></a>' +
        '</div>'
    });
}

function getNotifyClass(status){
    var alertClass = 'info';
    alertClass = status === 'success' ? 'success' : alertClass;
    alertClass = status === 'error' ? 'danger' : alertClass;
    return alertClass;
}

/*
 Parse json result
 */

function parseJSON(json)
{
    try
    {

        var jsonObject = JSON.parse(json);
        return jsonObject;
    }
    catch (e)
    {
        return json;
    }
}

function getAlertClass(status){
    var alertClass = 'alert alert-info';
    alertClass = status === 'success' ? 'alert alert-success' : alertClass;
    alertClass = status === 'error' ? 'alert alert-danger' : alertClass;
    return alertClass;
}

function pushUrl(title, url){
    var stateObject = { state:1 };
    document.title = title ? title : document.title;
//    history.pushState(stateObject, document.title, url);
    History.pushState(stateObject, title, url);
}

function setWindowUrl(){
    var windowUrl = $('#windowUrl').val() != undefined ? $('#windowUrl').val() : document.location.href;
    var title = $('#windowTitle').val() != undefined ? $('#windowTitle').val() : document.title;
    pushUrl(title, windowUrl);
}

/********************** HTML 5 attribute alternates *****************/
function WatermarkText() {
    if (!$.support.placeholder) {
        var active = document.activeElement;
        $('[placeholder]').focus(function() {
            if ($(this).attr('placeholder') != undefined && $(this).attr('placeholder') != '' && ($(this).val() == '' || $(this).val() == $(this).attr('placeholder'))) {
                //$(this).val() == '' - check is required here because the field is cleared off placeholder text on form submission
                $(this).val('').removeClass('hasPlaceholder');
            }
        }).blur(function() {
                if ($(this).attr('placeholder') != undefined && $(this).attr('placeholder') != '' && ($(this).val() == '' || $(this).val() == $(this).attr('placeholder'))) {
                    $(this).val($(this).attr('placeholder')).addClass('hasPlaceholder');
                }
            });
        $('[placeholder]').blur();
        $(active).focus();
        $('form').submit(function() {
            $(this).find('.hasPlaceholder').each(function() {
                $(this).val('');
                $(this).focus();
            });

        });
    }
}