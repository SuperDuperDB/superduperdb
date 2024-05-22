"use strict";(self.webpackChunknewdocs=self.webpackChunknewdocs||[]).push([[4721],{3698:(e,n,r)=>{r.r(n),r.d(n,{assets:()=>l,contentTitle:()=>c,default:()=>p,frontMatter:()=>i,metadata:()=>o,toc:()=>a});var t=r(4848),s=r(8453);const i={},c="VectorIndex",o={id:"apply_api/vector_index",title:"VectorIndex",description:"- Wrap a Listener so that outputs are searchable",source:"@site/content/apply_api/vector_index.md",sourceDirName:"apply_api",slug:"/apply_api/vector_index",permalink:"/docs/apply_api/vector_index",draft:!1,unlisted:!1,editUrl:"https://github.com/SuperDuperDB/superduperdb/blob/main/docs/hr/content/apply_api/vector_index.md",tags:[],version:"current",frontMatter:{},sidebar:"tutorialSidebar",previous:{title:"Listener",permalink:"/docs/apply_api/listener"},next:{title:"Stack",permalink:"/docs/apply_api/stack"}},l={},a=[];function d(e){const n={a:"a",code:"code",em:"em",h1:"h1",li:"li",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,s.R)(),...e.components};return(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(n.h1,{id:"vectorindex",children:(0,t.jsx)(n.code,{children:"VectorIndex"})}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsxs)(n.li,{children:["Wrap a ",(0,t.jsx)(n.code,{children:"Listener"})," so that outputs are searchable"]}),"\n",(0,t.jsxs)(n.li,{children:["Can optionally take a second ",(0,t.jsx)(n.code,{children:"Listener"})," for multimodal search"]}),"\n",(0,t.jsxs)(n.li,{children:["Applies to ",(0,t.jsx)(n.code,{children:"Listener"})," instances containing ",(0,t.jsx)(n.code,{children:"Model"})," instances which output vectors, arrays or tensors"]}),"\n",(0,t.jsxs)(n.li,{children:["Maybe leveraged in SuperDuperDB queries with the ",(0,t.jsx)(n.code,{children:".like"})," operator"]}),"\n"]}),"\n",(0,t.jsx)(n.p,{children:(0,t.jsx)(n.em,{children:(0,t.jsx)(n.strong,{children:"Dependencies"})})}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsx)(n.li,{children:(0,t.jsx)(n.code,{children:"Listener"})}),"\n"]}),"\n",(0,t.jsx)(n.p,{children:(0,t.jsx)(n.em,{children:(0,t.jsx)(n.strong,{children:"Usage pattern"})})}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-python",children:"from superduperdb import VectorIndex\n\nvi = VectorIndex(\n    'my-index',\n    indexing_listener=listener_1  # defined earlier calculates searchable vectors\n)\n\n# or directly from a model\nvi = model_1.to_vector_index(select=q, key='x')\n\n# or may use multiple listeners\nvi = VectorIndex(\n    'my-index',\n    indexing_listener=listener_1\n    compatible_listener=listener_2 # this listener can have `listener_2.active = False`\n)\n\ndb.apply(vi)\n"})}),"\n",(0,t.jsx)(n.p,{children:(0,t.jsx)(n.em,{children:(0,t.jsx)(n.strong,{children:"See also"})})}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsx)(n.li,{children:(0,t.jsx)(n.a,{href:"../query_api/vector_search",children:"vector-search queries"})}),"\n",(0,t.jsx)(n.li,{children:(0,t.jsx)(n.a,{href:"../cluster_mode/vector_comparison_service",children:"vector-search service"})}),"\n"]})]})}function p(e={}){const{wrapper:n}={...(0,s.R)(),...e.components};return n?(0,t.jsx)(n,{...e,children:(0,t.jsx)(d,{...e})}):d(e)}},8453:(e,n,r)=>{r.d(n,{R:()=>c,x:()=>o});var t=r(6540);const s={},i=t.createContext(s);function c(e){const n=t.useContext(i);return t.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function o(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(s):e.components||s:c(e.components),t.createElement(i.Provider,{value:n},e.children)}}}]);