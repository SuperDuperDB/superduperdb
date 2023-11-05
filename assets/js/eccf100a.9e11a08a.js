"use strict";(self.webpackChunknewdocs=self.webpackChunknewdocs||[]).push([[744],{3905:(e,n,t)=>{t.d(n,{Zo:()=>c,kt:()=>f});var r=t(67294);function o(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function a(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function i(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?a(Object(t),!0).forEach((function(n){o(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):a(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function s(e,n){if(null==e)return{};var t,r,o=function(e,n){if(null==e)return{};var t,r,o={},a=Object.keys(e);for(r=0;r<a.length;r++)t=a[r],n.indexOf(t)>=0||(o[t]=e[t]);return o}(e,n);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)t=a[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(o[t]=e[t])}return o}var p=r.createContext({}),d=function(e){var n=r.useContext(p),t=n;return e&&(t="function"==typeof e?e(n):i(i({},n),e)),t},c=function(e){var n=d(e.components);return r.createElement(p.Provider,{value:n},e.children)},m="mdxType",l={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},u=r.forwardRef((function(e,n){var t=e.components,o=e.mdxType,a=e.originalType,p=e.parentName,c=s(e,["components","mdxType","originalType","parentName"]),m=d(t),u=o,f=m["".concat(p,".").concat(u)]||m[u]||l[u]||a;return t?r.createElement(f,i(i({ref:n},c),{},{components:t})):r.createElement(f,i({ref:n},c))}));function f(e,n){var t=arguments,o=n&&n.mdxType;if("string"==typeof e||o){var a=t.length,i=new Array(a);i[0]=u;var s={};for(var p in n)hasOwnProperty.call(n,p)&&(s[p]=n[p]);s.originalType=e,s[m]="string"==typeof e?e:o,i[1]=s;for(var d=2;d<a;d++)i[d]=t[d];return r.createElement.apply(null,i)}return r.createElement.apply(null,t)}u.displayName="MDXCreateElement"},44362:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>p,contentTitle:()=>i,default:()=>l,frontMatter:()=>a,metadata:()=>s,toc:()=>d});var r=t(87462),o=(t(67294),t(3905));const a={},i="Search within videos with text",s={unversionedId:"use_cases/items/video_search",id:"use_cases/items/video_search",title:"Search within videos with text",description:"Create a superduperdb instance",source:"@site/content/use_cases/items/video_search.md",sourceDirName:"use_cases/items",slug:"/use_cases/items/video_search",permalink:"/docs/use_cases/items/video_search",draft:!1,editUrl:"https://github.com/SuperDuperDB/superduperdb/tree/main/docs/content/use_cases/items/video_search.md",tags:[],version:"current",frontMatter:{},sidebar:"useCasesSidebar",previous:{title:"MongoDB Atlas vector-search with SuperDuperDB",permalink:"/docs/use_cases/items/vector_search"},next:{title:"Cataloguing voice-memos for a self managed personal assistant",permalink:"/docs/use_cases/items/voice_memos"}},p={},d=[],c={toc:d},m="wrapper";function l(e){let{components:n,...t}=e;return(0,o.kt)(m,(0,r.Z)({},c,t,{components:n,mdxType:"MDXLayout"}),(0,o.kt)("h1",{id:"search-within-videos-with-text"},"Search within videos with text"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"!pip install superduperdb\n!pip install opencv-python\n!pip install git+https://github.com/openai/CLIP.git\n")),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"import cv2\nimport os\nimport requests\n\nimport clip\nimport glob\nfrom IPython.display import *\nimport numpy as np\nimport pymongo\nfrom PIL import Image\nimport torch\nfrom tqdm import tqdm\n\nfrom superduperdb import CFG\nfrom superduperdb import superduper\nfrom superduperdb.ext.pillow.image import pil_image\nfrom superduperdb.container.document import Document as D\nfrom superduperdb.container.model import Model\nfrom superduperdb.container.schema import Schema\nfrom superduperdb.db.mongodb.query import Collection\nfrom superduperdb.ext.torch.tensor import tensor\nfrom superduperdb.ext.torch.model import TorchModel\n")),(0,o.kt)("p",null,"Create a superduper",(0,o.kt)("inlineCode",{parentName:"p"},"db")," instance"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},'import os\n\n# Uncomment one of the following lines to use a bespoke MongoDB deployment\n# For testing the default connection is to mongomock\n\nmongodb_uri = os.getenv("MONGODB_URI","mongomock://test")\n# mongodb_uri = "mongodb://localhost:27017"\n# mongodb_uri = "mongodb://superduper:superduper@mongodb:27017/documents"\n# mongodb_uri = "mongodb://<user>:<pass>@<mongo_cluster>/<database>"\n# mongodb_uri = "mongodb+srv://<username>:<password>@<atlas_cluster>/<database>"\n\nCFG.downloads.hybrid = True\nCFG.downloads.root = \'./\'\n\n# Super-Duper your Database!\nfrom superduperdb import superduper\ndb = superduper(mongodb_uri)\n')),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"from superduperdb.container.encoder import Encoder\n\nvid_enc = Encoder(\n    identifier='video_on_file',\n    load_hybrid=False,\n)\n\ndb.add(vid_enc)\n")),(0,o.kt)("p",null,"Let's get a sample video from the net"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"db.execute(\n    Collection('videos')\n        .insert_one(\n            D({'video': vid_enc(uri='https://superduperdb-public.s3.eu-west-1.amazonaws.com/animals_excerpt.mp4')})\n        )\n)\n")),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"list(db.execute(Collection('video_frames').find()))\n")),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"import cv2\nimport numpy as np\nimport tqdm\n\n\ndef video2images(video_file):\n    sample_freq = 10\n    cap = cv2.VideoCapture(video_file)\n\n    prev_frame = None\n    frame_count = 0\n\n    fps = cap.get(cv2.CAP_PROP_FPS)\n    print(fps)\n    extracted_frames = []\n    progress = tqdm.tqdm()\n\n    while True:\n        ret, frame = cap.read()\n        if not ret:\n            break\n        current_timestamp = frame_count // fps\n        \n        if frame_count % sample_freq == 0:\n            extracted_frames.append({\n                'image': Image.fromarray(frame[:,:,::-1]),\n                'current_timestamp': current_timestamp,\n            })\n        frame_count += 1        \n        progress.update(1)\n    \n    cap.release()\n    cv2.destroyAllWindows()\n    return extracted_frames\n")),(0,o.kt)("p",null,"Create a Listener which will continously download video urls and save best frames into other collection."),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"from superduperdb.container.listener import Listener\n\nvideo2images = Model(\n    identifier='video2images',\n    object=video2images,\n    flatten=True,\n    model_update_kwargs={'document_embedded': False},\n    output_schema=Schema(identifier='myschema', fields={'image': pil_image})\n)\n\ndb.add(\n   Listener(\n       model=video2images,\n       select=Collection(name='videos').find(),\n       key='video',\n   )\n)\n")),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"db.execute(Collection('_outputs.video.video2images').find_one()).unpack()['_outputs']['video']['video2images']['image']\n")),(0,o.kt)("p",null,"Create CLIP model"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"model, preprocess = clip.load(\"RN50\", device='cpu')\nt = tensor(torch.float, shape=(1024,))\n\nvisual_model = TorchModel(\n    identifier='clip_image',\n    preprocess=preprocess,\n    object=model.visual,\n    encoder=t,\n)\ntext_model = TorchModel(\n    identifier='clip_text',\n    object=model,\n    preprocess=lambda x: clip.tokenize(x)[0],\n    forward_method='encode_text',\n    encoder=t,\n    device='cpu',\n    preferred_devices=None\n)\n")),(0,o.kt)("p",null,"Create VectorIndex with an indexing and compatible listener"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"from superduperdb.container.vector_index import VectorIndex\nfrom superduperdb.container.listener import Listener\nfrom superduperdb.ext.openai.model import OpenAIEmbedding\nfrom superduperdb.db.mongodb.query import Collection\n\ndb.add(\n    VectorIndex(\n        identifier='video_search_index',\n        indexing_listener=Listener(\n            model=visual_model,\n            key='_outputs.video.video2images.image',\n            select=Collection(name='_outputs.video.video2images').find(),\n        ),\n        compatible_listener=Listener(\n            model=text_model,\n            key='text',\n            select=None,\n            active=False\n        )\n    )\n)\n")),(0,o.kt)("p",null,"Test vector search by quering a text against saved frames."),(0,o.kt)("p",null,"Search for something that may have happened during the video:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"search_phrase = 'An elephant'\n\nr = next(db.execute(\n    Collection('_outputs.video.video2images').like(D({'text': 'An elephant'}), vector_index='video_search_index', n=1).find()\n))\n\nsearch_timestamp = r['_outputs']['video']['video2images']['current_timestamp']\n")),(0,o.kt)("p",null,"Get the back-reference to the original video document:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"video = db.execute(Collection('videos').find_one({'_id': r['_source']}))\n")),(0,o.kt)("p",null,"Start the video from the resultant timestamp:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},'from IPython.display import display, HTML\nvideo_html = f"""\n<video width="640" height="480" controls>\n    <source src="{video[\'video\'].uri}" type="video/mp4">\n</video>\n<script>\n    var video = document.querySelector(\'video\');\n    video.currentTime = {search_timestamp};\n    video.play();\n<\/script>\n"""\n\ndisplay(HTML(video_html))\n')))}l.isMDXComponent=!0}}]);