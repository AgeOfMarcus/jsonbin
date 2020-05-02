# jsonbin

A simple JSON storage bin with an open API. Demo server up at [https://jsonbin.marcusweinberger.repl.co](https://jsonbin.marcusweinberger.repl.co)

## Usage (python)

    import requests
    import json

    url = "https://jsonbin.marcusweinberger.repl.co/"
    token = requests.get(url).content.decode()
    uri = url + token + "/"

    data = {"hello": "world"}
    r = requests.post(uri + "test", data=json.dumps(data))
    print(r.status_code, r.content.decode())
    # 200 true

    print(requests.get(uri + "test").json())
    # {"hello": "world"}

    r = requests.delete(uri + "test")
    print(r.status_code, r.content.decode())
    # 200 true

