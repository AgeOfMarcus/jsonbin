from flask import Flask, jsonify, request
import json, uuid

class JsonBin(object):
    def __init__(self, dbfile="bin.json"):
        try:
            db = json.loads(open(dbfile, "r").read())
        except:
            db = {}
            with open(dbfile, "w") as f:
                f.write(json.dumps(db))
        finally:
            self.dbfile = dbfile
            self.db = db
    
    def _generate(self, leng=32):
        res = ""
        while len(res) < leng:
            res += str(uuid.uuid4()).replace("-","")
        return res[:leng]
    def _save(self):
        with open(self.dbfile, "w") as f:
            f.write(json.dumps(self.db))
    
    def store(self, token, key, data):
        if not token in self.db:
            self.db[token] = {}

        if not key in self.db[token]:
            self.db[token][key] = data
        else:
            self.db[token][key].update(data)
        
        self._save()
        return True
    
    def retrieve(self, token, key):
        return self.db.get(token, {}).get(key, None)
    
    def delete(self, token, key):
        if key in self.db.get(token, {}):
            del self.db[token][key]
            self._save()
            return True

def main(host="0.0.0.0", port=8080):
    app = Flask(__name__)
    jsonbin = JsonBin()

    @app.route("/")
    def app_index():
        return jsonbin._generate()
    
    @app.route("/<token>/<key>", methods=['GET','POST','DELETE'])
    def app_main(token, key):
        if request.method == "GET":
            res = jsonbin.retrieve(token, key)
        elif request.method == "POST":
            data = request.get_json(force=True)
            res = jsonbin.store(token, key, data)
        elif request.method == "DELETE":
            res = jsonbin.delete(token, key)
        
        try:
            return jsonify(res)
        except:
            return str(res)
    
    app.run(host=host, port=port)