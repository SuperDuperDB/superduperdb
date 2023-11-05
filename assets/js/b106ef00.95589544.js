"use strict";(self.webpackChunknewdocs=self.webpackChunknewdocs||[]).push([[3433],{3905:(e,t,r)=>{r.d(t,{Zo:()=>p,kt:()=>g});var a=r(67294);function n(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,a)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?o(Object(r),!0).forEach((function(t){n(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function s(e,t){if(null==e)return{};var r,a,n=function(e,t){if(null==e)return{};var r,a,n={},o=Object.keys(e);for(a=0;a<o.length;a++)r=o[a],t.indexOf(r)>=0||(n[r]=e[r]);return n}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)r=o[a],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(n[r]=e[r])}return n}var l=a.createContext({}),d=function(e){var t=a.useContext(l),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},p=function(e){var t=d(e.components);return a.createElement(l.Provider,{value:t},e.children)},c="mdxType",u={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},b=a.forwardRef((function(e,t){var r=e.components,n=e.mdxType,o=e.originalType,l=e.parentName,p=s(e,["components","mdxType","originalType","parentName"]),c=d(r),b=n,g=c["".concat(l,".").concat(b)]||c[b]||u[b]||o;return r?a.createElement(g,i(i({ref:t},p),{},{components:r})):a.createElement(g,i({ref:t},p))}));function g(e,t){var r=arguments,n=t&&t.mdxType;if("string"==typeof e||n){var o=r.length,i=new Array(o);i[0]=b;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s[c]="string"==typeof e?e:n,i[1]=s;for(var d=2;d<o;d++)i[d]=r[d];return a.createElement.apply(null,i)}return a.createElement.apply(null,r)}b.displayName="MDXCreateElement"},669:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>l,contentTitle:()=>i,default:()=>u,frontMatter:()=>o,metadata:()=>s,toc:()=>d});var a=r(87462),n=(r(67294),r(3905));const o={sidebar_position:16},i="Working with and inserting large pieces of data",s={unversionedId:"docs/using_hybrid_storage_to_handle_large_data_blobs",id:"docs/using_hybrid_storage_to_handle_large_data_blobs",title:"Working with and inserting large pieces of data",description:"Some applications require large data-blobs and objects, which are larger than the objects which are supported by the underlying database.",source:"@site/content/docs/16_using_hybrid_storage_to_handle_large_data_blobs.md",sourceDirName:"docs",slug:"/docs/using_hybrid_storage_to_handle_large_data_blobs",permalink:"/docs/docs/using_hybrid_storage_to_handle_large_data_blobs",draft:!1,editUrl:"https://github.com/SuperDuperDB/superduperdb/tree/main/docs/content/docs/16_using_hybrid_storage_to_handle_large_data_blobs.md",tags:[],version:"current",sidebarPosition:16,frontMatter:{sidebar_position:16},sidebar:"tutorialSidebar",previous:{title:"Working with external data sources",permalink:"/docs/docs/referring_to_data_from_diverse_sources"},next:{title:"Interfacing with popular AI frameworks",permalink:"/docs/docs/supported_ai_frameworks"}},l={},d=[],p={toc:d},c="wrapper";function u(e){let{components:t,...r}=e;return(0,n.kt)(c,(0,a.Z)({},p,r,{components:t,mdxType:"MDXLayout"}),(0,n.kt)("h1",{id:"working-with-and-inserting-large-pieces-of-data"},"Working with and inserting large pieces of data"),(0,n.kt)("p",null,"Some applications require large data-blobs and objects, which are larger than the objects which are supported by the underlying database."),(0,n.kt)("p",null,"For example:"),(0,n.kt)("ul",null,(0,n.kt)("li",{parentName:"ul"},"MongoDB supports documents up to ",(0,n.kt)("inlineCode",{parentName:"li"},"16MB")),(0,n.kt)("li",{parentName:"ul"},"SQLite ",(0,n.kt)("inlineCode",{parentName:"li"},"BINARY")," has a default limit of ",(0,n.kt)("inlineCode",{parentName:"li"},"1GB"))),(0,n.kt)("p",null,"In addition, for some applications, which are very read-heavy (for example training CNN on a database of images), storing data directly in the database, can lead to impaired database performance."),(0,n.kt)("p",null,"In such cases, ",(0,n.kt)("inlineCode",{parentName:"p"},"superduperdb")," supports hybrid storage, where large data blobs, are stored on the local filesystem."),(0,n.kt)("p",null,(0,n.kt)("inlineCode",{parentName:"p"},"superduperdb")," supports this hybrid storage, via ",(0,n.kt)("inlineCode",{parentName:"p"},"env")," variable or configuration:"),(0,n.kt)("pre",null,(0,n.kt)("code",{parentName:"pre",className:"language-python"},"CFG.downloads.hybrid = True\n")),(0,n.kt)("p",null,"...or"),(0,n.kt)("pre",null,(0,n.kt)("code",{parentName:"pre",className:"language-bash"},"export SUPERDUPERDB_DOWNLOADS_HYBRID=true\n")),(0,n.kt)("p",null,"Once this has been configured, inserting data proceeds exactly as before, with the difference\nthat items inserted via URI, are saved on the local filesystem, and referred to in the database."),(0,n.kt)("p",null,"Read ",(0,n.kt)("a",{parentName:"p",href:"/docs/docs/referring_to_data_from_diverse_sources"},"here")," for more details."))}u.isMDXComponent=!0}}]);