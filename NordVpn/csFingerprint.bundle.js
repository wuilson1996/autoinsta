!function(){try{var t="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:{},e=Error().stack;e&&(t._sentryDebugIds=t._sentryDebugIds||{},t._sentryDebugIds[e]="9790de84-3a42-44f0-8e88-ff296c6ede34",t._sentryDebugIdIdentifier="sentry-dbid-9790de84-3a42-44f0-8e88-ff296c6ede34")}catch(t){}}();var _global="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:{};_global.SENTRY_RELEASE={id:"4.6.3"},(()=>{var t={38341:(t,e,n)=>{"use strict";function s(){return"undefined"!=typeof __SENTRY_BROWSER_BUNDLE__&&!!__SENTRY_BROWSER_BUNDLE__}n.d(e,{Z:()=>s})},36284:(t,e,n)=>{"use strict";n.d(e,{fj:()=>o,wD:()=>r});var s=n(38341);t=n.hmd(t);var i=n(65606);function r(){return!(0,s.Z)()&&"[object process]"===Object.prototype.toString.call(void 0!==i?i:0)}function o(t,e){return t.require(e)}},89297:(t,e,n)=>{"use strict";n.d(e,{lu:()=>c,zf:()=>d});var s=n(36284),i=n(16341);t=n.hmd(t);let r=(0,i.VZ)(),o={nowSeconds:()=>Date.now()/1e3},a=(0,s.wD)()?function(){try{return(0,s.fj)(t,"perf_hooks").performance}catch(t){return}}():function(){let{performance:t}=r;if(t&&t.now)return{now:()=>t.now(),timeOrigin:Date.now()-t.now()}}(),u=void 0===a?o:{nowSeconds:()=>(a.timeOrigin+a.now())/1e3},c=o.nowSeconds.bind(o),d=u.nowSeconds.bind(u);(()=>{let{performance:t}=r;if(!t||!t.now)return;let e=t.now(),n=Date.now(),s=t.timeOrigin?Math.abs(t.timeOrigin+e-n):36e5,i=t.timing&&t.timing.navigationStart,o="number"==typeof i?Math.abs(i+e-n):36e5;if(s<36e5||o<36e5)return s<=o?t.timeOrigin:void 0})()},16341:(t,e,n)=>{"use strict";function s(t){return t&&t.Math==Math?t:void 0}n.d(e,{BY:()=>o,OW:()=>i,VZ:()=>r});let i="object"==typeof globalThis&&s(globalThis)||"object"==typeof window&&s(window)||"object"==typeof self&&s(self)||"object"==typeof n.g&&s(n.g)||function(){return this}()||{};function r(){return i}function o(t,e,n){let s=n||i,r=s.__SENTRY__=s.__SENTRY__||{};return r[t]||(r[t]=e())}},65606:t=>{var e,n,s,i=t.exports={};function r(){throw Error("setTimeout has not been defined")}function o(){throw Error("clearTimeout has not been defined")}function a(t){if(e===setTimeout)return setTimeout(t,0);if((e===r||!e)&&setTimeout)return e=setTimeout,setTimeout(t,0);try{return e(t,0)}catch(n){try{return e.call(null,t,0)}catch(n){return e.call(this,t,0)}}}!function(){try{e="function"==typeof setTimeout?setTimeout:r}catch(t){e=r}try{n="function"==typeof clearTimeout?clearTimeout:o}catch(t){n=o}}();var u=[],c=!1,d=-1;function l(){c&&s&&(c=!1,s.length?u=s.concat(u):d=-1,u.length&&h())}function h(){if(!c){var t=a(l);c=!0;for(var e=u.length;e;){for(s=u,u=[];++d<e;)s&&s[d].run();d=-1,e=u.length}s=null,c=!1,function(t){if(n===clearTimeout)return clearTimeout(t);if((n===o||!n)&&clearTimeout)return n=clearTimeout,clearTimeout(t);try{n(t)}catch(e){try{return n.call(null,t)}catch(e){return n.call(this,t)}}}(t)}}function _(t,e){this.fun=t,this.array=e}function p(){}i.nextTick=function(t){var e=Array(arguments.length-1);if(arguments.length>1)for(var n=1;n<arguments.length;n++)e[n-1]=arguments[n];u.push(new _(t,e)),1!==u.length||c||a(h)},_.prototype.run=function(){this.fun.apply(null,this.array)},i.title="browser",i.browser=!0,i.env={},i.argv=[],i.version="",i.versions={},i.on=p,i.addListener=p,i.once=p,i.off=p,i.removeListener=p,i.removeAllListeners=p,i.emit=p,i.prependListener=p,i.prependOnceListener=p,i.listeners=function(t){return[]},i.binding=function(t){throw Error("process.binding is not supported")},i.cwd=function(){return"/"},i.chdir=function(t){throw Error("process.chdir is not supported")},i.umask=function(){return 0}}},e={};function n(s){var i=e[s];if(void 0!==i)return i.exports;var r=e[s]={id:s,loaded:!1,exports:{}};return t[s](r,r.exports,n),r.loaded=!0,r.exports}n.d=(t,e)=>{for(var s in e)n.o(e,s)&&!n.o(t,s)&&Object.defineProperty(t,s,{enumerable:!0,get:e[s]})},n.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||Function("return this")()}catch(t){if("object"==typeof window)return window}}(),n.hmd=t=>((t=Object.create(t)).children||(t.children=[]),Object.defineProperty(t,"exports",{enumerable:!0,set:()=>{throw Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+t.id)}}),t),n.o=(t,e)=>Object.prototype.hasOwnProperty.call(t,e),(()=>{"use strict";let t;var e,s,i=n(16341);function r(){let t=i.OW,e=t.crypto||t.msCrypto;if(e&&e.randomUUID)return e.randomUUID().replace(/-/g,"");let n=e&&e.getRandomValues?()=>e.getRandomValues(new Uint8Array(1))[0]:()=>16*Math.random();return"10000000100040008000100000000000".replace(/[018]/g,t=>(t^(15&n())>>t/4).toString(16))}var o=n(89297);let a=["debug","info","warn","error","log","assert","trace"];function u(t){if(!("console"in i.OW))return t();let e=i.OW.console,n={};a.forEach(t=>{let s=e[t]&&e[t].__sentry_original__;t in e&&s&&(n[t]=e[t],e[t]=s)});try{return t()}finally{Object.keys(n).forEach(t=>{e[t]=n[t]})}}function c(){let t=!1,e={enable:()=>{t=!0},disable:()=>{t=!1}};return"undefined"==typeof __SENTRY_DEBUG__||__SENTRY_DEBUG__?a.forEach(n=>{e[n]=(...e)=>{t&&u(()=>{i.OW.console[n](`Sentry Logger [${n}]:`,...e)})}}):a.forEach(t=>{e[t]=()=>void 0}),e}"undefined"==typeof __SENTRY_DEBUG__||__SENTRY_DEBUG__?t=(0,i.BY)("logger",c):t=c();let d=Object.prototype.toString;function l(t){return"[object Object]"===d.call(t)}function h(t){return!!(t&&t.then&&"function"==typeof t.then)}!function(t){t[t.PENDING=0]="PENDING",t[t.RESOLVED=1]="RESOLVED",t[t.REJECTED=2]="REJECTED"}(e||(e={}));class _{constructor(t){_.prototype.__init.call(this),_.prototype.__init2.call(this),_.prototype.__init3.call(this),_.prototype.__init4.call(this),this._state=e.PENDING,this._handlers=[];try{t(this._resolve,this._reject)}catch(t){this._reject(t)}}then(t,e){return new _((n,s)=>{this._handlers.push([!1,e=>{if(t)try{n(t(e))}catch(t){s(t)}else n(e)},t=>{if(e)try{n(e(t))}catch(t){s(t)}else s(t)}]),this._executeHandlers()})}catch(t){return this.then(t=>t,t)}finally(t){return new _((e,n)=>{let s,i;return this.then(e=>{i=!1,s=e,t&&t()},e=>{i=!0,s=e,t&&t()}).then(()=>{if(i){n(s);return}e(s)})})}__init(){this._resolve=t=>{this._setResult(e.RESOLVED,t)}}__init2(){this._reject=t=>{this._setResult(e.REJECTED,t)}}__init3(){this._setResult=(t,n)=>{if(this._state===e.PENDING){if(h(n)){n.then(this._resolve,this._reject);return}this._state=t,this._value=n,this._executeHandlers()}}}__init4(){this._executeHandlers=()=>{if(this._state===e.PENDING)return;let t=this._handlers.slice();this._handlers=[],t.forEach(t=>{t[0]||(this._state===e.RESOLVED&&t[1](this._value),this._state===e.REJECTED&&t[2](this._value),t[0]=!0)})}}}function p(t,e={}){if(!e.user||(!t.ipAddress&&e.user.ip_address&&(t.ipAddress=e.user.ip_address),t.did||e.did||(t.did=e.user.id||e.user.email||e.user.username)),t.timestamp=e.timestamp||(0,o.zf)(),e.ignoreDuration&&(t.ignoreDuration=e.ignoreDuration),e.sid&&(t.sid=32===e.sid.length?e.sid:r()),void 0!==e.init&&(t.init=e.init),!t.did&&e.did&&(t.did=`${e.did}`),"number"==typeof e.started&&(t.started=e.started),t.ignoreDuration)t.duration=void 0;else if("number"==typeof e.duration)t.duration=e.duration;else{let e=t.timestamp-t.started;t.duration=e>=0?e:0}e.release&&(t.release=e.release),e.environment&&(t.environment=e.environment),!t.ipAddress&&e.ipAddress&&(t.ipAddress=e.ipAddress),!t.userAgent&&e.userAgent&&(t.userAgent=e.userAgent),"number"==typeof e.errors&&(t.errors=e.errors),e.status&&(t.status=e.status)}class f{constructor(){this._notifyingListeners=!1,this._scopeListeners=[],this._eventProcessors=[],this._breadcrumbs=[],this._attachments=[],this._user={},this._tags={},this._extra={},this._contexts={},this._sdkProcessingMetadata={},this._propagationContext=g()}static clone(t){let e=new f;return t&&(e._breadcrumbs=[...t._breadcrumbs],e._tags={...t._tags},e._extra={...t._extra},e._contexts={...t._contexts},e._user=t._user,e._level=t._level,e._span=t._span,e._session=t._session,e._transactionName=t._transactionName,e._fingerprint=t._fingerprint,e._eventProcessors=[...t._eventProcessors],e._requestSession=t._requestSession,e._attachments=[...t._attachments],e._sdkProcessingMetadata={...t._sdkProcessingMetadata},e._propagationContext={...t._propagationContext}),e}addScopeListener(t){this._scopeListeners.push(t)}addEventProcessor(t){return this._eventProcessors.push(t),this}setUser(t){return this._user=t||{},this._session&&p(this._session,{user:t}),this._notifyScopeListeners(),this}getUser(){return this._user}getRequestSession(){return this._requestSession}setRequestSession(t){return this._requestSession=t,this}setTags(t){return this._tags={...this._tags,...t},this._notifyScopeListeners(),this}setTag(t,e){return this._tags={...this._tags,[t]:e},this._notifyScopeListeners(),this}setExtras(t){return this._extra={...this._extra,...t},this._notifyScopeListeners(),this}setExtra(t,e){return this._extra={...this._extra,[t]:e},this._notifyScopeListeners(),this}setFingerprint(t){return this._fingerprint=t,this._notifyScopeListeners(),this}setLevel(t){return this._level=t,this._notifyScopeListeners(),this}setTransactionName(t){return this._transactionName=t,this._notifyScopeListeners(),this}setContext(t,e){return null===e?delete this._contexts[t]:this._contexts[t]=e,this._notifyScopeListeners(),this}setSpan(t){return this._span=t,this._notifyScopeListeners(),this}getSpan(){return this._span}getTransaction(){let t=this.getSpan();return t&&t.transaction}setSession(t){return t?this._session=t:delete this._session,this._notifyScopeListeners(),this}getSession(){return this._session}update(t){if(!t)return this;if("function"==typeof t){let e=t(this);return e instanceof f?e:this}return t instanceof f?(this._tags={...this._tags,...t._tags},this._extra={...this._extra,...t._extra},this._contexts={...this._contexts,...t._contexts},t._user&&Object.keys(t._user).length&&(this._user=t._user),t._level&&(this._level=t._level),t._fingerprint&&(this._fingerprint=t._fingerprint),t._requestSession&&(this._requestSession=t._requestSession),t._propagationContext&&(this._propagationContext=t._propagationContext)):l(t)&&(this._tags={...this._tags,...t.tags},this._extra={...this._extra,...t.extra},this._contexts={...this._contexts,...t.contexts},t.user&&(this._user=t.user),t.level&&(this._level=t.level),t.fingerprint&&(this._fingerprint=t.fingerprint),t.requestSession&&(this._requestSession=t.requestSession),t.propagationContext&&(this._propagationContext=t.propagationContext)),this}clear(){return this._breadcrumbs=[],this._tags={},this._extra={},this._user={},this._contexts={},this._level=void 0,this._transactionName=void 0,this._fingerprint=void 0,this._requestSession=void 0,this._span=void 0,this._session=void 0,this._notifyScopeListeners(),this._attachments=[],this._propagationContext=g(),this}addBreadcrumb(t,e){let n="number"==typeof e?e:100;if(n<=0)return this;let s={timestamp:(0,o.lu)(),...t};return this._breadcrumbs=[...this._breadcrumbs,s].slice(-n),this._notifyScopeListeners(),this}getLastBreadcrumb(){return this._breadcrumbs[this._breadcrumbs.length-1]}clearBreadcrumbs(){return this._breadcrumbs=[],this._notifyScopeListeners(),this}addAttachment(t){return this._attachments.push(t),this}getAttachments(){return this._attachments}clearAttachments(){return this._attachments=[],this}applyToEvent(t,e={}){if(this._extra&&Object.keys(this._extra).length&&(t.extra={...this._extra,...t.extra}),this._tags&&Object.keys(this._tags).length&&(t.tags={...this._tags,...t.tags}),this._user&&Object.keys(this._user).length&&(t.user={...this._user,...t.user}),this._contexts&&Object.keys(this._contexts).length&&(t.contexts={...this._contexts,...t.contexts}),this._level&&(t.level=this._level),this._transactionName&&(t.transaction=this._transactionName),this._span){t.contexts={trace:this._span.getTraceContext(),...t.contexts};let e=this._span.transaction;if(e){t.sdkProcessingMetadata={dynamicSamplingContext:e.getDynamicSamplingContext(),...t.sdkProcessingMetadata};let n=e.name;n&&(t.tags={transaction:n,...t.tags})}}return this._applyFingerprint(t),t.breadcrumbs=[...t.breadcrumbs||[],...this._breadcrumbs],t.breadcrumbs=t.breadcrumbs.length>0?t.breadcrumbs:void 0,t.sdkProcessingMetadata={...t.sdkProcessingMetadata,...this._sdkProcessingMetadata,propagationContext:this._propagationContext},this._notifyEventProcessors([...(0,i.BY)("globalEventProcessors",()=>[]),...this._eventProcessors],t,e)}setSDKProcessingMetadata(t){return this._sdkProcessingMetadata={...this._sdkProcessingMetadata,...t},this}setPropagationContext(t){return this._propagationContext=t,this}getPropagationContext(){return this._propagationContext}_notifyEventProcessors(e,n,s,i=0){return new _((r,o)=>{let a=e[i];if(null===n||"function"!=typeof a)r(n);else{let u=a({...n},s);("undefined"==typeof __SENTRY_DEBUG__||__SENTRY_DEBUG__)&&a.id&&null===u&&t.log(`Event processor "${a.id}" dropped event`),h(u)?u.then(t=>this._notifyEventProcessors(e,t,s,i+1).then(r)).then(null,o):this._notifyEventProcessors(e,u,s,i+1).then(r).then(null,o)}})}_notifyScopeListeners(){this._notifyingListeners||(this._notifyingListeners=!0,this._scopeListeners.forEach(t=>{t(this)}),this._notifyingListeners=!1)}_applyFingerprint(t){var e;t.fingerprint=t.fingerprint?Array.isArray(e=t.fingerprint)?e:[e]:[],this._fingerprint&&(t.fingerprint=t.fingerprint.concat(this._fingerprint)),t.fingerprint&&!t.fingerprint.length&&delete t.fingerprint}}function g(){return{traceId:r(),spanId:r().substring(16)}}class m{constructor(t,e=new f,n=4){this._version=n,this._stack=[{scope:e}],t&&this.bindClient(t)}isOlderThan(t){return this._version<t}bindClient(t){this.getStackTop().client=t,t&&t.setupIntegrations&&t.setupIntegrations()}pushScope(){let t=f.clone(this.getScope());return this.getStack().push({client:this.getClient(),scope:t}),t}popScope(){return!(this.getStack().length<=1)&&!!this.getStack().pop()}withScope(t){let e=this.pushScope();try{t(e)}finally{this.popScope()}}getClient(){return this.getStackTop().client}getScope(){return this.getStackTop().scope}getStack(){return this._stack}getStackTop(){return this._stack[this._stack.length-1]}captureException(t,e){let n=this._lastEventId=e&&e.event_id?e.event_id:r(),s=Error("Sentry syntheticException");return this._withClient((i,r)=>{i.captureException(t,{originalException:t,syntheticException:s,...e,event_id:n},r)}),n}captureMessage(t,e,n){let s=this._lastEventId=n&&n.event_id?n.event_id:r(),i=Error(t);return this._withClient((r,o)=>{r.captureMessage(t,e,{originalException:t,syntheticException:i,...n,event_id:s},o)}),s}captureEvent(t,e){let n=e&&e.event_id?e.event_id:r();return t.type||(this._lastEventId=n),this._withClient((s,i)=>{s.captureEvent(t,{...e,event_id:n},i)}),n}lastEventId(){return this._lastEventId}addBreadcrumb(t,e){let{scope:n,client:s}=this.getStackTop();if(!s)return;let{beforeBreadcrumb:i=null,maxBreadcrumbs:r=100}=s.getOptions&&s.getOptions()||{};if(r<=0)return;let a={timestamp:(0,o.lu)(),...t},c=i?u(()=>i(a,e)):a;null!==c&&(s.emit&&s.emit("beforeAddBreadcrumb",c,e),n.addBreadcrumb(c,r))}setUser(t){this.getScope().setUser(t)}setTags(t){this.getScope().setTags(t)}setExtras(t){this.getScope().setExtras(t)}setTag(t,e){this.getScope().setTag(t,e)}setExtra(t,e){this.getScope().setExtra(t,e)}setContext(t,e){this.getScope().setContext(t,e)}configureScope(t){let{scope:e,client:n}=this.getStackTop();n&&t(e)}run(t){let e=y(this);try{t(this)}finally{y(e)}}getIntegration(e){let n=this.getClient();if(!n)return null;try{return n.getIntegration(e)}catch(n){return("undefined"==typeof __SENTRY_DEBUG__||__SENTRY_DEBUG__)&&t.warn(`Cannot retrieve integration ${e.id} from the current Hub`),null}}startTransaction(t,e){let n=this._callExtensionMethod("startTransaction",t,e);return("undefined"==typeof __SENTRY_DEBUG__||__SENTRY_DEBUG__)&&!n&&(this.getClient()?console.warn(`Tracing extension 'startTransaction' has not been added. Call 'addTracingExtensions' before calling 'init':
Sentry.addTracingExtensions();
Sentry.init({...});
`):console.warn("Tracing extension 'startTransaction' is missing. You should 'init' the SDK before calling 'startTransaction'")),n}traceHeaders(){return this._callExtensionMethod("traceHeaders")}captureSession(t=!1){if(t)return this.endSession();this._sendSessionUpdate()}endSession(){let t=this.getStackTop().scope,e=t.getSession();if(e){let t;t={},"ok"===e.status&&(t={status:"exited"}),p(e,t)}this._sendSessionUpdate(),t.setSession()}startSession(t){let{scope:e,client:n}=this.getStackTop(),{release:s,environment:a="production"}=n&&n.getOptions()||{},{userAgent:u}=i.OW.navigator||{},c=function(t){let e=(0,o.zf)(),n={sid:r(),init:!0,timestamp:e,started:e,duration:0,status:"ok",errors:0,ignoreDuration:!1,toJSON:()=>(function t(e,n){if(l(e)){let s=n.get(e);if(void 0!==s)return s;let i={};for(let s of(n.set(e,i),Object.keys(e)))void 0!==e[s]&&(i[s]=t(e[s],n));return i}if(Array.isArray(e)){let s=n.get(e);if(void 0!==s)return s;let i=[];return n.set(e,i),e.forEach(e=>{i.push(t(e,n))}),i}return e})({sid:`${n.sid}`,init:n.init,started:new Date(1e3*n.started).toISOString(),timestamp:new Date(1e3*n.timestamp).toISOString(),status:n.status,errors:n.errors,did:"number"==typeof n.did||"string"==typeof n.did?`${n.did}`:void 0,duration:n.duration,attrs:{release:n.release,environment:n.environment,ip_address:n.ipAddress,user_agent:n.userAgent}},new Map)};return t&&p(n,t),n}({release:s,environment:a,user:e.getUser(),...u&&{userAgent:u},...t}),d=e.getSession&&e.getSession();return d&&"ok"===d.status&&p(d,{status:"exited"}),this.endSession(),e.setSession(c),c}shouldSendDefaultPii(){let t=this.getClient(),e=t&&t.getOptions();return!!(e&&e.sendDefaultPii)}_sendSessionUpdate(){let{scope:t,client:e}=this.getStackTop(),n=t.getSession();n&&e&&e.captureSession&&e.captureSession(n)}_withClient(t){let{scope:e,client:n}=this.getStackTop();n&&t(n,e)}_callExtensionMethod(e,...n){let s=S().__SENTRY__;if(s&&s.extensions&&"function"==typeof s.extensions[e])return s.extensions[e].apply(this,n);("undefined"==typeof __SENTRY_DEBUG__||__SENTRY_DEBUG__)&&t.warn(`Extension method ${e} couldn't be found, doing nothing.`)}}function S(){return i.OW.__SENTRY__=i.OW.__SENTRY__||{extensions:{},hub:void 0},i.OW}function y(t){let e=S(),n=v(e);return E(e,t),n}function b(){let t=S();if(t.__SENTRY__&&t.__SENTRY__.acs){let e=t.__SENTRY__.acs.getCurrentHub();if(e)return e}return function(t=S()){var e;return(!((e=t)&&e.__SENTRY__&&e.__SENTRY__.hub)||v(t).isOlderThan(4))&&E(t,new m),v(t)}(t)}function v(t){return(0,i.BY)("hub",()=>new m,t)}function E(t,e){return!!t&&((t.__SENTRY__=t.__SENTRY__||{}).hub=e,!0)}var x=new Uint8Array(16);let w=/^(?:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}|00000000-0000-0000-0000-000000000000)$/i;for(var T=[],R=0;R<256;++R)T.push((R+256).toString(16).substr(1));let N=function(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0,n=(T[t[e+0]]+T[t[e+1]]+T[t[e+2]]+T[t[e+3]]+"-"+T[t[e+4]]+T[t[e+5]]+"-"+T[t[e+6]]+T[t[e+7]]+"-"+T[t[e+8]]+T[t[e+9]]+"-"+T[t[e+10]]+T[t[e+11]]+T[t[e+12]]+T[t[e+13]]+T[t[e+14]]+T[t[e+15]]).toLowerCase();if(!("string"==typeof n&&w.test(n)))throw TypeError("Stringified UUID is invalid");return n},D=globalThis;var C=n(65606);let O=String("4.6.3"),L="beta"===String("prod");String(L?"https://59af6e99d78d6968ba004b3a2794f5bd@debug.nordvpn.com/48":"https://f392de5db1154edba05b3c7dd6209162@debug.nordvpn.com/19"),String(L?"https://1ba6d9f128b476dc25572b722cfe39e5@debug.nordvpn.com/51":"https://7467962fcaf84800bb56b3ead8935a19@debug.nordvpn.com/20"),String(L?"https://a73dc2baab9fc3272ce09820bd97f425@debug.nordvpn.com/49":"https://2e30719d0c124f4e88ffdddd56ec5776@debug.nordvpn.com/40"),O.replace(/\./g,"-"),C.env.APP_REVIEW_MODE;let P=String("chrome"),k="firefox"===P;["chrome","edge"].includes(P),C.env.APP_DISABLE_STORAGE_CACHE,function(t){var e=(t=t||{}).random||(t.rng||function(){if(!s&&!(s="undefined"!=typeof crypto&&crypto.getRandomValues&&crypto.getRandomValues.bind(crypto)||"undefined"!=typeof msCrypto&&"function"==typeof msCrypto.getRandomValues&&msCrypto.getRandomValues.bind(msCrypto)))throw Error("crypto.getRandomValues() not supported. See https://github.com/uuidjs/uuid#getrandomvalues-not-supported");return s(x)})();e[6]=15&e[6]|64,e[8]=63&e[8]|128,N(e)}(),/OPR\//i.test(D.navigator.userAgent);let A=k?browser:chrome;async function U(t,{reportExceptions:e}){try{return await A.runtime.sendMessage(t)}catch(t){if(e){var n;n=e=>{e.setFingerprint(["BROWSER.runtime.sendMessage"]),b().captureException(t,{captureContext:void 0})},b().withScope(n)}return}}async function Y(){let t=["Arial","Times New Roman","Courier New"],e={},n=await new Promise(t=>{document.body?t(document.body):document.addEventListener("DOMContentLoaded",()=>{t(document.body)})});for(let s=0;s<t.length;s+=1){let i=t[s],r=document.createElement("span");r.style.fontFamily=i,r.style.visibility="hidden",r.style.position="absolute",r.style.top="0",r.style.left="0",r.textContent="nordvpn",n.appendChild(r);let o=r.getBoundingClientRect(),a={width:o.width,height:o.height,left:o.left,top:o.top};e[i]=a,document.body.removeChild(r)}return e}new URL(A.runtime.getURL("")).protocol,(async()=>{let t=await Promise.allSettled([new Promise(t=>t(function(){let t=document.createElement("canvas").getContext("webgl"),e=null==t?void 0:t.getParameter(t.RENDERER);return{renderer:e,vendor:null==t?void 0:t.getParameter(t.VENDOR),version:null==t?void 0:t.getParameter(t.VERSION),shadingLanguageVersion:null==t?void 0:t.getParameter(t.SHADING_LANGUAGE_VERSION)}}())),function(){let t=document.createElement("canvas"),e=t.getContext("2d"),n="NordVPN,com <canvas> 1.0";return e&&(e.textBaseline="top",e.font="14px 'Arial'",e.textBaseline="alphabetic",e.fillStyle="#f60",e.fillRect(125,1,62,20),e.fillStyle="#069",e.fillText(n,2,15),e.fillStyle="rgba(102, 204, 0, 0.7)",e.fillText(n,4,17)),t.toDataURL()}(),new Promise(t=>t({accelerometer:"LinearAccelerationSensor"in window,gyroscope:"Gyroscope"in window,magnetometer:"Magnetometer"in window,ambientLightSensor:"AmbientLightSensor"in window,proximitySensor:"ProximitySensor"in window})),Y()]);U(JSON.parse(JSON.stringify({webGL:"fulfilled"===t[0].status?t[0].value:void 0,canvas:"fulfilled"===t[1].status?t[1].value:void 0,sensors:"fulfilled"===t[2].status?t[2].value:void 0,fonts:"fulfilled"===t[3].status?t[3].value:void 0})),{reportExceptions:!1})})()})()})();