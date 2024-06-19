"use strict";(self.webpackChunknewdocs=self.webpackChunknewdocs||[]).push([[7339],{3506:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>u,contentTitle:()=>i,default:()=>p,frontMatter:()=>s,metadata:()=>c,toc:()=>d});var o=t(4848),r=t(8453);const s={},i="MongoDB select queries",c={id:"execute_api/mongodb_queries",title:"MongoDB select queries",description:"SuperDuperDB supports the pymongo query API to build select queries.",source:"@site/content/execute_api/mongodb_queries.md",sourceDirName:"execute_api",slug:"/execute_api/mongodb_queries",permalink:"/docs/execute_api/mongodb_queries",draft:!1,unlisted:!1,editUrl:"https://github.com/SuperDuperDB/superduperdb/blob/main/docs/hr/content/execute_api/mongodb_queries.md",tags:[],version:"current",frontMatter:{},sidebar:"tutorialSidebar",previous:{title:"Selecting data",permalink:"/docs/execute_api/select_queries"},next:{title:"SQL select queries",permalink:"/docs/execute_api/sql_queries"}},u={},d=[];function l(e){const n={code:"code",h1:"h1",p:"p",pre:"pre",...(0,r.R)(),...e.components};return(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(n.h1,{id:"mongodb-select-queries",children:"MongoDB select queries"}),"\n",(0,o.jsxs)(n.p,{children:["SuperDuperDB supports the ",(0,o.jsx)(n.code,{children:"pymongo"})," query API to build select queries.\nThere is one slight difference however, since queries built with ",(0,o.jsx)(n.code,{children:"pymongo"}),"'s formalism\nare executed lazily:"]}),"\n",(0,o.jsxs)(n.p,{children:["Whereas in ",(0,o.jsx)(n.code,{children:"pymongo"})," one might write:"]}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-python",children:"client.my_db.my_collection.find_one()\n"})}),"\n",(0,o.jsxs)(n.p,{children:["with ",(0,o.jsx)(n.code,{children:"superduperdb"})," one would write:"]}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-python",children:"result = db['my_collection'].find_one().execute()\n"})})]})}function p(e={}){const{wrapper:n}={...(0,r.R)(),...e.components};return n?(0,o.jsx)(n,{...e,children:(0,o.jsx)(l,{...e})}):l(e)}},8453:(e,n,t)=>{t.d(n,{R:()=>i,x:()=>c});var o=t(6540);const r={},s=o.createContext(r);function i(e){const n=o.useContext(s);return o.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function c(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(r):e.components||r:i(e.components),o.createElement(s.Provider,{value:n},e.children)}}}]);