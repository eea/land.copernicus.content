$(document).ready(function() {

// sameTimeLimit (https://github.com/IonicaBizau/same-time-limit)
"use strict";

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

(function (f) {
    if ((typeof exports === "undefined" ? "undefined" : _typeof(exports)) === "object" && typeof module !== "undefined") {
        module.exports = f();
    } else if (typeof define === "function" && define.amd) {
        define([], f);
    } else {
        var g;if (typeof window !== "undefined") {
            g = window;
        } else if (typeof global !== "undefined") {
            g = global;
        } else if (typeof self !== "undefined") {
            g = self;
        } else {
            g = this;
        }g.sameTimeLimit = f();
    }
})(function () {
    var define, module, exports;return function e(t, n, r) {
        function s(o, u) {
            if (!n[o]) {
                if (!t[o]) {
                    var a = typeof require == "function" && require;if (!u && a) return a(o, !0);if (i) return i(o, !0);var f = new Error("Cannot find module '" + o + "'");throw f.code = "MODULE_NOT_FOUND", f;
                }var l = n[o] = { exports: {} };t[o][0].call(l.exports, function (e) {
                    var n = t[o][1][e];return s(n ? n : e);
                }, l, l.exports, e, t, n, r);
            }return n[o].exports;
        }var i = typeof require == "function" && require;for (var o = 0; o < r.length; o++) {
            s(r[o]);
        }return s;
    }({ 1: [function (require, module, exports) {
            // shim for using process in browser
            var process = module.exports = {};

            // cached from whatever global is present so that test runners that stub it
            // don't break things.  But we need to wrap it in a try catch in case it is
            // wrapped in strict mode code which doesn't define any globals.  It's inside a
            // function because try/catches deoptimize in certain engines.

            var cachedSetTimeout;
            var cachedClearTimeout;

            function defaultSetTimout() {
                throw new Error('setTimeout has not been defined');
            }
            function defaultClearTimeout() {
                throw new Error('clearTimeout has not been defined');
            }
            (function () {
                try {
                    if (typeof setTimeout === 'function') {
                        cachedSetTimeout = setTimeout;
                    } else {
                        cachedSetTimeout = defaultSetTimout;
                    }
                } catch (e) {
                    cachedSetTimeout = defaultSetTimout;
                }
                try {
                    if (typeof clearTimeout === 'function') {
                        cachedClearTimeout = clearTimeout;
                    } else {
                        cachedClearTimeout = defaultClearTimeout;
                    }
                } catch (e) {
                    cachedClearTimeout = defaultClearTimeout;
                }
            })();
            function runTimeout(fun) {
                if (cachedSetTimeout === setTimeout) {
                    //normal enviroments in sane situations
                    return setTimeout(fun, 0);
                }
                // if setTimeout wasn't available but was latter defined
                if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
                    cachedSetTimeout = setTimeout;
                    return setTimeout(fun, 0);
                }
                try {
                    // when when somebody has screwed with setTimeout but no I.E. maddness
                    return cachedSetTimeout(fun, 0);
                } catch (e) {
                    try {
                        // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
                        return cachedSetTimeout.call(null, fun, 0);
                    } catch (e) {
                        // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
                        return cachedSetTimeout.call(this, fun, 0);
                    }
                }
            }
            function runClearTimeout(marker) {
                if (cachedClearTimeout === clearTimeout) {
                    //normal enviroments in sane situations
                    return clearTimeout(marker);
                }
                // if clearTimeout wasn't available but was latter defined
                if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
                    cachedClearTimeout = clearTimeout;
                    return clearTimeout(marker);
                }
                try {
                    // when when somebody has screwed with setTimeout but no I.E. maddness
                    return cachedClearTimeout(marker);
                } catch (e) {
                    try {
                        // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
                        return cachedClearTimeout.call(null, marker);
                    } catch (e) {
                        // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
                        // Some versions of I.E. have different rules for clearTimeout vs setTimeout
                        return cachedClearTimeout.call(this, marker);
                    }
                }
            }
            var queue = [];
            var draining = false;
            var currentQueue;
            var queueIndex = -1;

            function cleanUpNextTick() {
                if (!draining || !currentQueue) {
                    return;
                }
                draining = false;
                if (currentQueue.length) {
                    queue = currentQueue.concat(queue);
                } else {
                    queueIndex = -1;
                }
                if (queue.length) {
                    drainQueue();
                }
            }

            function drainQueue() {
                if (draining) {
                    return;
                }
                var timeout = runTimeout(cleanUpNextTick);
                draining = true;

                var len = queue.length;
                while (len) {
                    currentQueue = queue;
                    queue = [];
                    while (++queueIndex < len) {
                        if (currentQueue) {
                            currentQueue[queueIndex].run();
                        }
                    }
                    queueIndex = -1;
                    len = queue.length;
                }
                currentQueue = null;
                draining = false;
                runClearTimeout(timeout);
            }

            process.nextTick = function (fun) {
                var args = new Array(arguments.length - 1);
                if (arguments.length > 1) {
                    for (var i = 1; i < arguments.length; i++) {
                        args[i - 1] = arguments[i];
                    }
                }
                queue.push(new Item(fun, args));
                if (queue.length === 1 && !draining) {
                    runTimeout(drainQueue);
                }
            };

            // v8 likes predictible objects
            function Item(fun, array) {
                this.fun = fun;
                this.array = array;
            }
            Item.prototype.run = function () {
                this.fun.apply(null, this.array);
            };
            process.title = 'browser';
            process.browser = true;
            process.env = {};
            process.argv = [];
            process.version = ''; // empty string to avoid regexp issues
            process.versions = {};

            function noop() {}

            process.on = noop;
            process.addListener = noop;
            process.once = noop;
            process.off = noop;
            process.removeListener = noop;
            process.removeAllListeners = noop;
            process.emit = noop;

            process.binding = function (name) {
                throw new Error('process.binding is not supported');
            };

            process.cwd = function () {
                return '/';
            };
            process.chdir = function (dir) {
                throw new Error('process.chdir is not supported');
            };
            process.umask = function () {
                return 0;
            };
        }, {}], 2: [function (require, module, exports) {
            "use strict";

            var sameTime = require("same-time"),
                limitIt = require("limit-it");

            /**
             * sameTimeLimit
             * Runs async tasks in parallel but not more than a given limit in
             * the same time.
             *
             * @name sameTimeLimit
             * @function
             * @param {Array} tasks An array of async functions to call. Their first
             * parameter should be the callback function.
             * @param {Number} limit The max count of functions to run in parallel.
             * @param {Function} cb The callback function.
             * @param {Array} store An optional array to store the data in. If `null`, data won't be stored.
             * @returns {LimitIt} The `LimitIt` instance.
             */
            module.exports = function sameTimeLimit(tasks, limit, cb, store) {
                var l = new limitIt(limit);
                sameTime(tasks.map(function (c) {
                    return function (done) {
                        l.add(c, done);
                    };
                }), cb, store);
                return l;
            };
        }, { "limit-it": 3, "same-time": 7 }], 3: [function (require, module, exports) {
            "use strict";

            // Dependencies

            var Typpy = require("typpy");

            // Constants
            var DEFAULT_LIMIT = 50;

            /*!
             * BuffElm
             * Creates a `BuffElm` instance.
             *
             * @name BuffElm
             * @function
             * @param {Function} func The function to be called.
             * @param {Array} args The arguments passed to the function.
             * @param {Function} callback The callback function.
             * @return {BuffElm} The `BuffElm` instance.
             */
            function BuffElm(func, args, callback) {
                this._ = func;
                this.callback = callback;
                this.args = args || [];

                // 0: initial state
                // 1: running
                // 2: done
                this.state = 0;
            }

            /**
             * LimitIt
             * Creates a new instance of `LimitIt`.
             *
             * @name LimitIt
             * @function
             * @param {Number} limit The limit value representing the number of functions
             * that are run in parallel at a moment of time.
             * @return {LimitIt} The `LimitIt` instance.
             */
            function LimitIt(limit) {

                if (Typpy(this) !== "limitit") {
                    return new LimitIt(limit);
                }

                limit = limit || DEFAULT_LIMIT;

                this.limit = limit;
                this.buffer = [];
                this.running = 0;
            }

            /**
             * add
             * Adds a new function in the buffer.
             *
             * @name add
             * @function
             * @param {Function} func The function to be run.
             * @param {Array} args The arguments passed to the function.
             * @param {Function} callback The callback function.
             * @return {LimitIt} The `LimitIt` instance.
             */
            LimitIt.prototype.add = function (func, args, callback) {

                if (typeof args === "function") {
                    callback = args;
                    args = [];
                }

                this.buffer.push(new BuffElm(func, args, callback));
                return this.check();
            };

            /**
             * exceeded
             * Checks if the limit was exceeded.
             *
             * @name exceeded
             * @function
             * @return {Boolean} `true` if the limit was exceeded, otherwise `false`.
             */
            LimitIt.prototype.exceeded = function () {
                return this.running >= this.limit;
            };

            /**
             * check
             * Checks and runs the functions from the buffer.
             *
             * @name check
             * @function
             * @return {LimitIt} The `LimitIt` instance.
             */
            LimitIt.prototype.check = function () {

                var self = this,
                    i = 0,
                    c = null;

                if (self.exceeded()) {
                    return self;
                }

                for (; i < self.buffer.length; ++i) {
                    c = self.buffer[i];
                    if (c.state !== 0) {
                        continue;
                    }
                    ++self.running;
                    self.run(c);
                    if (self.exceeded()) {
                        break;
                    }
                }

                return self;
            };

            /**
             * run
             * Runs the function from the buffer element.
             *
             * @name run
             * @function
             * @param {BuffElm} c The buffer element to run.
             * @return {LimitIt} The `LimitIt` instance.
             */
            LimitIt.prototype.run = function (c) {
                var self = this;
                if (c.state !== 0) debugger;

                // Push the callback function
                c.args.push(function () {
                    c.state = 2;
                    --self.running;
                    c.callback.apply(self, arguments);
                    self.check();
                });

                c.state = 1;
                c._.apply(self, c.args);

                return self;
            };

            module.exports = LimitIt;
        }, { "typpy": 4 }], 4: [function (require, module, exports) {
            "use strict";

            require("function.name");

            /**
             * Typpy
             * Gets the type of the input value or compares it
             * with a provided type.
             *
             * Usage:
             *
             * ```js
             * Typpy({}) // => "object"
             * Typpy(42, Number); // => true
             * Typpy.get([], "array"); => true
             * ```
             *
             * @name Typpy
             * @function
             * @param {Anything} input The input value.
             * @param {Constructor|String} target The target type.
             * It could be a string (e.g. `"array"`) or a
             * constructor (e.g. `Array`).
             * @return {String|Boolean} It returns `true` if the
             * input has the provided type `target` (if was provided),
             * `false` if the input type does *not* have the provided type
             * `target` or the stringified type of the input (always lowercase).
             */
            function Typpy(input, target) {
                if (arguments.length === 2) {
                    return Typpy.is(input, target);
                }
                return Typpy.get(input, true);
            }

            /**
             * Typpy.is
             * Checks if the input value has a specified type.
             *
             * @name Typpy.is
             * @function
             * @param {Anything} input The input value.
             * @param {Constructor|String} target The target type.
             * It could be a string (e.g. `"array"`) or a
             * constructor (e.g. `Array`).
             * @return {Boolean} `true`, if the input has the same
             * type with the target or `false` otherwise.
             */
            Typpy.is = function (input, target) {
                return Typpy.get(input, typeof target === "string") === target;
            };

            /**
             * Typpy.get
             * Gets the type of the input value. This is used internally.
             *
             * @name Typpy.get
             * @function
             * @param {Anything} input The input value.
             * @param {Boolean} str A flag to indicate if the return value
             * should be a string or not.
             * @return {Constructor|String} The input value constructor
             * (if any) or the stringified type (always lowercase).
             */
            Typpy.get = function (input, str) {

                if (typeof input === "string") {
                    return str ? "string" : String;
                }

                if (null === input) {
                    return str ? "null" : null;
                }

                if (undefined === input) {
                    return str ? "undefined" : undefined;
                }

                if (input !== input) {
                    return str ? "nan" : NaN;
                }

                return str ? input.constructor.name.toLowerCase() : input.constructor;
            };

            module.exports = Typpy;
        }, { "function.name": 5 }], 5: [function (require, module, exports) {
            "use strict";

            var noop6 = require("noop6");

            (function () {
                var NAME_FIELD = "name";

                if (typeof noop6.name === "string") {
                    return;
                }

                try {
                    Object.defineProperty(Function.prototype, NAME_FIELD, {
                        get: function get() {
                            var name = this.toString().trim().match(/^function\s*([^\s(]+)/)[1];
                            Object.defineProperty(this, NAME_FIELD, { value: name });
                            return name;
                        }
                    });
                } catch (e) {}
            })();

            /**
             * functionName
             * Get the function name.
             *
             * @name functionName
             * @function
             * @param {Function} input The input function.
             * @returns {String} The function name.
             */
            module.exports = function functionName(input) {
                return input.name;
            };
        }, { "noop6": 6 }], 6: [function (require, module, exports) {
            "use strict";

            module.exports = function () {};
        }, {}], 7: [function (require, module, exports) {
            (function (process) {
                "use strict";

                var deffy = require("deffy");

                /**
                 * sameTime
                 * Calls functions in parallel and stores the results.
                 *
                 * @name sameTime
                 * @function
                 * @param {Array} arr An array of functions getting the callback parameter in the first argument.
                 * @param {Function} cb The callback function called with:
                 *
                 *  - first parameter: `null` if there were no errors or an array containing the error values
                 *  - `1 ... n` parameters: arrays containing the callback results
                 *
                 * @param {Array} store An optional array to store the data in. If `null`, data won't be stored.
                 * @return {sameTime} The `sameTime` function.
                 */
                module.exports = function sameTime(arr, cb, store) {

                    var result = store,
                        complete = 0,
                        length = arr.length;

                    if (cb) {
                        if (result === undefined) {
                            result = [];
                        }
                    } else {
                        result = null;
                    }

                    if (!arr.length) {
                        return process.nextTick(cb.bind(null, null, []));
                    }

                    // Run functions
                    arr.forEach(function (c, index) {
                        var _done = false;

                        // Call the current function
                        c(function () {

                            if (_done) {
                                return;
                            }
                            _done = true;

                            var args = [].slice.call(arguments),
                                cRes = null,
                                i = 0;

                            if (result) {
                                // Prepare the result data
                                for (; i < args.length; ++i) {
                                    cRes = result[i] = deffy(result[i], []);
                                    cRes[index] = args[i];
                                }
                            }

                            // Check if all functions send the responses
                            if (++complete !== length) {
                                return;
                            }
                            if (result) {
                                if (!deffy(result[0], []).filter(Boolean).length) {
                                    result[0] = null;
                                }
                            }
                            cb && cb.apply(null, result);
                        });
                    });
                };
            }).call(this, require('_process'));
        }, { "_process": 1, "deffy": 8 }], 8: [function (require, module, exports) {
            // Dependencies
            var Typpy = require("typpy");

            /**
             * Deffy
             * Computes a final value by providing the input and default values.
             *
             * @name Deffy
             * @function
             * @param {Anything} input The input value.
             * @param {Anything|Function} def The default value or a function getting the
             * input value as first argument.
             * @param {Object|Boolean} options The `empty` value or an object containing
             * the following fields:
             *
             *  - `empty` (Boolean): Handles the input value as empty field (`input || default`). Default is `false`.
             *
             * @return {Anything} The computed value.
             */
            function Deffy(input, def, options) {

                // Default is a function
                if (typeof def === "function") {
                    return def(input);
                }

                options = Typpy(options) === "boolean" ? {
                    empty: options
                } : {
                    empty: false
                };

                // Handle empty
                if (options.empty) {
                    return input || def;
                }

                // Return input
                if (Typpy(input) === Typpy(def)) {
                    return input;
                }

                // Return the default
                return def;
            }

            module.exports = Deffy;
        }, { "typpy": 9 }], 9: [function (require, module, exports) {
            arguments[4][4][0].apply(exports, arguments);
        }, { "dup": 4, "function.name": 10 }], 10: [function (require, module, exports) {
            arguments[4][5][0].apply(exports, arguments);
        }, { "dup": 5, "noop6": 11 }], 11: [function (require, module, exports) {
            arguments[4][6][0].apply(exports, arguments);
        }, { "dup": 6 }] }, {}, [2])(2);
});

"use strict";

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

(function (f) {
    if ((typeof exports === "undefined" ? "undefined" : _typeof(exports)) === "object" && typeof module !== "undefined") {
        module.exports = f();
    } else if (typeof define === "function" && define.amd) {
        define([], f);
    } else {
        var g;if (typeof window !== "undefined") {
            g = window;
        } else if (typeof global !== "undefined") {
            g = global;
        } else if (typeof self !== "undefined") {
            g = self;
        } else {
            g = this;
        }g.bindy = f();
    }
})(function () {
    var define, module, exports;return function e(t, n, r) {
        function s(o, u) {
            if (!n[o]) {
                if (!t[o]) {
                    var a = typeof require == "function" && require;if (!u && a) return a(o, !0);if (i) return i(o, !0);var f = new Error("Cannot find module '" + o + "'");throw f.code = "MODULE_NOT_FOUND", f;
                }var l = n[o] = { exports: {} };t[o][0].call(l.exports, function (e) {
                    var n = t[o][1][e];return s(n ? n : e);
                }, l, l.exports, e, t, n, r);
            }return n[o].exports;
        }var i = typeof require == "function" && require;for (var o = 0; o < r.length; o++) {
            s(r[o]);
        }return s;
    }({ 1: [function (require, module, exports) {
            var sliced = require("sliced"),
                deffy = require("deffy");

            /**
             * bindy
             * Creates an array of functions bound to the specified arrays.
             *
             * @name bindy
             * @function
             * @param {Array} arr An array of elements.
             * @param {Function} fn The function to use for binding.
             * @return {Array} An array of functions. Each function is bound to the current
             * element from the input array.
             */
            module.exports = function bindy(arr, cb) {
                arr = deffy(arr, []);
                return arr.map(function (c, index, arr) {
                    return function () {
                        var args = sliced(arguments);
                        args.unshift(c);
                        return cb.apply(this, args);
                    };
                });
            };
        }, { "deffy": 2, "sliced": 6 }], 2: [function (require, module, exports) {
            // Dependencies
            var Typpy = require("typpy");

            /**
             * Deffy
             * Computes a final value by providing the input and default values.
             *
             * @name Deffy
             * @function
             * @param {Anything} input The input value.
             * @param {Anything|Function} def The default value or a function getting the
             * input value as first argument.
             * @param {Object|Boolean} options The `empty` value or an object containing
             * the following fields:
             *
             *  - `empty` (Boolean): Handles the input value as empty field (`input || default`). Default is `false`.
             *
             * @return {Anything} The computed value.
             */
            function Deffy(input, def, options) {

                // Default is a function
                if (typeof def === "function") {
                    return def(input);
                }

                options = Typpy(options) === "boolean" ? {
                    empty: options
                } : {
                    empty: false
                };

                // Handle empty
                if (options.empty) {
                    return input || def;
                }

                // Return input
                if (Typpy(input) === Typpy(def)) {
                    return input;
                }

                // Return the default
                return def;
            }

            module.exports = Deffy;
        }, { "typpy": 3 }], 3: [function (require, module, exports) {
            "use strict";

            require("function.name");

            /**
             * Typpy
             * Gets the type of the input value or compares it
             * with a provided type.
             *
             * Usage:
             *
             * ```js
             * Typpy({}) // => "object"
             * Typpy(42, Number); // => true
             * Typpy.get([], "array"); => true
             * ```
             *
             * @name Typpy
             * @function
             * @param {Anything} input The input value.
             * @param {Constructor|String} target The target type.
             * It could be a string (e.g. `"array"`) or a
             * constructor (e.g. `Array`).
             * @return {String|Boolean} It returns `true` if the
             * input has the provided type `target` (if was provided),
             * `false` if the input type does *not* have the provided type
             * `target` or the stringified type of the input (always lowercase).
             */
            function Typpy(input, target) {
                if (arguments.length === 2) {
                    return Typpy.is(input, target);
                }
                return Typpy.get(input, true);
            }

            /**
             * Typpy.is
             * Checks if the input value has a specified type.
             *
             * @name Typpy.is
             * @function
             * @param {Anything} input The input value.
             * @param {Constructor|String} target The target type.
             * It could be a string (e.g. `"array"`) or a
             * constructor (e.g. `Array`).
             * @return {Boolean} `true`, if the input has the same
             * type with the target or `false` otherwise.
             */
            Typpy.is = function (input, target) {
                return Typpy.get(input, typeof target === "string") === target;
            };

            /**
             * Typpy.get
             * Gets the type of the input value. This is used internally.
             *
             * @name Typpy.get
             * @function
             * @param {Anything} input The input value.
             * @param {Boolean} str A flag to indicate if the return value
             * should be a string or not.
             * @return {Constructor|String} The input value constructor
             * (if any) or the stringified type (always lowercase).
             */
            Typpy.get = function (input, str) {

                if (typeof input === "string") {
                    return str ? "string" : String;
                }

                if (null === input) {
                    return str ? "null" : null;
                }

                if (undefined === input) {
                    return str ? "undefined" : undefined;
                }

                if (input !== input) {
                    return str ? "nan" : NaN;
                }

                return str ? input.constructor.name.toLowerCase() : input.constructor;
            };

            module.exports = Typpy;
        }, { "function.name": 4 }], 4: [function (require, module, exports) {
            "use strict";

            var noop6 = require("noop6");

            (function () {
                var NAME_FIELD = "name";

                if (typeof noop6.name === "string") {
                    return;
                }

                try {
                    Object.defineProperty(Function.prototype, NAME_FIELD, {
                        get: function get() {
                            var name = this.toString().trim().match(/^function\s*([^\s(]+)/)[1];
                            Object.defineProperty(this, NAME_FIELD, { value: name });
                            return name;
                        }
                    });
                } catch (e) {}
            })();

            /**
             * functionName
             * Get the function name.
             *
             * @name functionName
             * @function
             * @param {Function} input The input function.
             * @returns {String} The function name.
             */
            module.exports = function functionName(input) {
                return input.name;
            };
        }, { "noop6": 5 }], 5: [function (require, module, exports) {
            "use strict";

            module.exports = function () {};
        }, {}], 6: [function (require, module, exports) {

            /**
             * An Array.prototype.slice.call(arguments) alternative
             *
             * @param {Object} args something with a length
             * @param {Number} slice
             * @param {Number} sliceEnd
             * @api public
             */

            module.exports = function (args, slice, sliceEnd) {
                var ret = [];
                var len = args.length;

                if (0 === len) return ret;

                var start = slice < 0 ? Math.max(0, slice + len) : slice || 0;

                if (sliceEnd !== undefined) {
                    len = sliceEnd < 0 ? sliceEnd + len : sliceEnd;
                }

                while (len-- > start) {
                    ret[len - start] = args[len];
                }

                return ret;
            };
        }, {}] }, {}, [1])(1);
});


  // Download file
  function download_file(url, cb) {
    return $.fileDownload(url).done(function() {
        // GOOGLE ANALYTICS custom event
        // Custom dimensions
        ga('set', 'dimension1', professional_thematic_domain);
        ga('set', 'dimension2', institutional_domain);
        ga('set', 'dimension3', is_eionet_member);

        // Track event
        ga('send', {
          'hitType': 'event',                 // Required.
          'eventCategory': 'page',            // Required.
          'eventAction': 'landfile_download', // Required.
          'eventLabel': land_item_title,
          'eventValue': 1
        });

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
  sameTimeLimit(bindy(files, download_file), 3, function () {});
});
