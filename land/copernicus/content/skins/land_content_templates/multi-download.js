$(document).ready(function() {
  // [TODO] Send the GA custom event for each file

/*

 http://localhost:8081/copernicus/local/urban-atlas/urban-atlas-2012/@@redirect-download-url?selected=@barlad@tulcea@la-linea-de-la-concepcion@ceuta@alytus@aviles@torrevieja@santa-lucia-de-tirajana@alphen-aan-den-rijn@eastbourne@siauliai?selected=@barlad

?selected=
@barlad
@tulcea
@la-linea-de-la-concepcion
@ceuta@alytus
@aviles
@torrevieja
@santa-lucia-de-tirajana
@alphen-aan-den-rijn
@eastbourne@siauliai
?selected=@barlad

*/

// sameTimeLimit (https://github.com/IonicaBizau/same-time-limit)
!function(t){if("object"==typeof exports&&"undefined"!=typeof module)module.exports=t();else if("function"==typeof define&&define.amd)define([],t);else{var n;n="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:this,n.sameTimeLimit=t()}}(function(){return function t(n,e,r){function i(u,c){if(!e[u]){if(!n[u]){var f="function"==typeof require&&require;if(!c&&f)return f(u,!0);if(o)return o(u,!0);var s=new Error("Cannot find module '"+u+"'");throw s.code="MODULE_NOT_FOUND",s}var a=e[u]={exports:{}};n[u][0].call(a.exports,function(t){var e=n[u][1][t];return i(e?e:t)},a,a.exports,t,n,e,r)}return e[u].exports}for(var o="function"==typeof require&&require,u=0;u<r.length;u++)i(r[u]);return i}({1:[function(t,n,e){function r(){throw new Error("setTimeout has not been defined")}function i(){throw new Error("clearTimeout has not been defined")}function o(t){if(l===setTimeout)return setTimeout(t,0);if((l===r||!l)&&setTimeout)return l=setTimeout,setTimeout(t,0);try{return l(t,0)}catch(n){try{return l.call(null,t,0)}catch(n){return l.call(this,t,0)}}}function u(t){if(p===clearTimeout)return clearTimeout(t);if((p===i||!p)&&clearTimeout)return p=clearTimeout,clearTimeout(t);try{return p(t)}catch(n){try{return p.call(null,t)}catch(n){return p.call(this,t)}}}function c(){m&&d&&(m=!1,d.length?y=d.concat(y):g=-1,y.length&&f())}function f(){if(!m){var t=o(c);m=!0;for(var n=y.length;n;){for(d=y,y=[];++g<n;)d&&d[g].run();g=-1,n=y.length}d=null,m=!1,u(t)}}function s(t,n){this.fun=t,this.array=n}function a(){}var l,p,h=n.exports={};!function(){try{l="function"==typeof setTimeout?setTimeout:r}catch(t){l=r}try{p="function"==typeof clearTimeout?clearTimeout:i}catch(t){p=i}}();var d,y=[],m=!1,g=-1;h.nextTick=function(t){var n=new Array(arguments.length-1);if(arguments.length>1)for(var e=1;e<arguments.length;e++)n[e-1]=arguments[e];y.push(new s(t,n)),1!==y.length||m||o(f)},s.prototype.run=function(){this.fun.apply(null,this.array)},h.title="browser",h.browser=!0,h.env={},h.argv=[],h.version="",h.versions={},h.on=a,h.addListener=a,h.once=a,h.off=a,h.removeListener=a,h.removeAllListeners=a,h.emit=a,h.binding=function(t){throw new Error("process.binding is not supported")},h.cwd=function(){return"/"},h.chdir=function(t){throw new Error("process.chdir is not supported")},h.umask=function(){return 0}},{}],2:[function(t,n,e){"use strict";var r=t("same-time"),i=t("limit-it");n.exports=function(t,n,e,o){var u=new i(n);return r(t.map(function(t){return function(n){u.add(t,n)}}),e,o),u}},{"limit-it":3,"same-time":7}],3:[function(t,n,e){"use strict";function r(t,n,e){this._=t,this.callback=e,this.args=n||[],this.state=0}function i(t){return"limitit"!==o(this)?new i(t):(t=t||u,this.limit=t,this.buffer=[],void(this.running=0))}var o=t("typpy"),u=50;i.prototype.add=function(t,n,e){return"function"==typeof n&&(e=n,n=[]),this.buffer.push(new r(t,n,e)),this.check()},i.prototype.exceeded=function(){return this.running>=this.limit},i.prototype.check=function(){var t=this,n=0,e=null;if(t.exceeded())return t;for(;n<t.buffer.length&&(e=t.buffer[n],0!==e.state||(++t.running,t.run(e),!t.exceeded()));++n);return t},i.prototype.run=function(t){var n=this;return 0!==t.state,t.args.push(function(){t.state=2,--n.running,t.callback.apply(n,arguments),n.check()}),t.state=1,t._.apply(n,t.args),n},n.exports=i},{typpy:4}],4:[function(t,n,e){"use strict";function r(t,n){return 2===arguments.length?r.is(t,n):r.get(t,!0)}t("function.name"),r.is=function(t,n){return r.get(t,"string"==typeof n)===n},r.get=function(t,n){return"string"==typeof t?n?"string":String:null===t?n?"null":null:void 0===t?n?"undefined":void 0:t!==t?n?"nan":NaN:n?t.constructor.name.toLowerCase():t.constructor},n.exports=r},{"function.name":5}],5:[function(t,n,e){"use strict";var r=t("noop6");!function(){var t="name";"string"!=typeof r.name&&Object.defineProperty(Function.prototype,t,{get:function(){var n=this.toString().trim().match(/^function\s*([^\s(]+)/)[1];return Object.defineProperty(this,t,{value:n}),n}})}(),n.exports=function(t){return t.name}},{noop6:6}],6:[function(t,n,e){"use strict";n.exports=function(){}},{}],7:[function(t,n,e){(function(e){"use strict";var r=t("deffy");n.exports=function(t,n,i){var o=i,u=0,c=t.length;return n?void 0===o&&(o=[]):o=null,t.length?void t.forEach(function(t,e){var i=!1;t(function(){if(!i){i=!0;var t=[].slice.call(arguments),f=null,s=0;if(o)for(;s<t.length;++s)f=o[s]=r(o[s],[]),f[e]=t[s];++u===c&&(o&&(r(o[0],[]).filter(Boolean).length||(o[0]=null)),n&&n.apply(null,o))}})}):e.nextTick(n.bind(null,null,[]))}}).call(this,t("_process"))},{_process:1,deffy:8}],8:[function(t,n,e){function r(t,n,e){return"function"==typeof n?n(t):(e="boolean"===i(e)?{empty:e}:{empty:!1},e.empty?t||n:i(t)===i(n)?t:n)}var i=t("typpy");n.exports=r},{typpy:9}],9:[function(t,n,e){arguments[4][4][0].apply(e,arguments)},{dup:4,"function.name":10}],10:[function(t,n,e){arguments[4][5][0].apply(e,arguments)},{dup:5,noop6:11}],11:[function(t,n,e){arguments[4][6][0].apply(e,arguments)},{dup:6}]},{},[2])(2)});

// bindy (https://github.com/IonicaBizau/bindy)
!function(n){if("object"==typeof exports&&"undefined"!=typeof module)module.exports=n();else if("function"==typeof define&&define.amd)define([],n);else{var t;t="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:this,t.bindy=n()}}(function(){return function n(t,e,r){function o(u,f){if(!e[u]){if(!t[u]){var c="function"==typeof require&&require;if(!f&&c)return c(u,!0);if(i)return i(u,!0);var s=new Error("Cannot find module '"+u+"'");throw s.code="MODULE_NOT_FOUND",s}var p=e[u]={exports:{}};t[u][0].call(p.exports,function(n){var e=t[u][1][n];return o(e?e:n)},p,p.exports,n,t,e,r)}return e[u].exports}for(var i="function"==typeof require&&require,u=0;u<r.length;u++)o(r[u]);return o}({1:[function(n,t,e){"use strict";var r=n("sliced"),o=n("deffy");t.exports=function(n,t){return n=o(n,[]),n.map(function(n,e,o){return function(){var e=r(arguments);return e.unshift(n),t.apply(this,e)}})}},{deffy:2,sliced:6}],2:[function(n,t,e){function r(n,t,e){return"function"==typeof t?t(n):(e="boolean"===o(e)?{empty:e}:{empty:!1},e.empty?n||t:o(n)===o(t)?n:t)}var o=n("typpy");t.exports=r},{typpy:3}],3:[function(n,t,e){"use strict";function r(n,t){return 2===arguments.length?r.is(n,t):r.get(n,!0)}n("function.name"),r.is=function(n,t){return r.get(n,"string"==typeof t)===t},r.get=function(n,t){return"string"==typeof n?t?"string":String:null===n?t?"null":null:void 0===n?t?"undefined":void 0:n!==n?t?"nan":NaN:t?n.constructor.name.toLowerCase():n.constructor},t.exports=r},{"function.name":4}],4:[function(n,t,e){"use strict";var r=n("noop6");!function(){var n="name";"string"!=typeof r.name&&Object.defineProperty(Function.prototype,n,{get:function(){var t=this.toString().trim().match(/^function\s*([^\s(]+)/)[1];return Object.defineProperty(this,n,{value:t}),t}})}(),t.exports=function(n){return n.name}},{noop6:5}],5:[function(n,t,e){"use strict";t.exports=function(){}},{}],6:[function(n,t,e){t.exports=function(n,t,e){var r=[],o=n.length;if(0===o)return r;var i=t<0?Math.max(0,t+o):t||0;for(void 0!==e&&(o=e<0?e+o:e);o-- >i;)r[o-i]=n[o];return r}},{}]},{},[1])(1)});

  // Download file
  function download_file(url. cb) {
    console.log("Downloading " + url)
    return $.fileDownload(url).done(function() {
        cb();
    }).fail(function() {
        cb();
    });
  }

  /* [TODO] Upgrade step to rewrite all these links or replace them in python code? */
  files_str = files_str.split("https://cws-download.eea.europa.eu").join("http://demo.copernicus.eea.europa.eu/filedownload");

  // Get the list of files
  var files = files_str.split(',');

  // Download the files in parallel, with a limit of 5 files at the time.
  sameTimeLimit(bindy(files, download_file), 5, function () {});
});
