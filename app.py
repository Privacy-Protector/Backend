from db import db
from db import Situation, Tag, Request
from flask import Flask, request
import json
import os



app = Flask(__name__)
db_filename = "privacy-protector.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code = 200):
    return json.dumps({"success": True, "data": data}), code
def failure_response(message, code = 404):
    return json.dumps({"success": False, "error": message}), code


@app.route("/")
def hello_world():
    return "Hello world!"

# ----------- USER ROUTES -------------------------------------------------------------------

@app.route("/api/events/")
def get_all_situations():
    return success_response([s.serialize() for s in Situation.query.all()])



@app.route("/api/situations/tag/")
def get_all_stuations_tag():
    body = json.loads(request.data)
    tag = body.get("tag")      
    response = []
    for s in Situation.query.all():
        for t in s.tag:
            if t.title == tag:
                response.append(s.serialize())                        
    return success_response(response)



@app.route("/api/situation/<int:id>/")
def get_situation(id): 
    body = json.loads(request.data)
    situation = Situation.query.filter_by(id = id).first()          
    if situation is None:
        return failure_response("Situation not found!")  
    return success_response(situation.serialize())


@app.route("/api/tag/", methods=['POST'])
def create_tag():
    body = json.loads(request.data)
    title = body.get("title")
    if title is None:
        return failure_response("Invalid field!")
    new_tag = Tag(title = title)
    db.session.add(new_tag)
    db.session.commit()
    return success_response(new_tag.serialize(), 201)


@app.route("/api/situations/whitelist/<int:id>", methods=['POST'])
def add_company_to_whitelist():
    
    body = json.loads(request.data)   
    company = body.get("company")
    situation = Situation.query.filter_by(id = id).first() 
    if situation is None:
        return failure_response("Situation not found!")

    wL = Whitelist(name = name) 
    db.session.add(wL)
    situation.whitelist.append(wL)
    db.session.commit()


@app.route("/api/situations/send/", methods=['POST'])
def send_situation_request():
    
    body = json.loads(request.data)   
    path = body.get("path")
    info = body.get("info")
    solution = body.get("solution")
    law = body.get("law")
   
    if path is None or info is None:
        return failure_response("Invalid field!")
  
    new_request = Request(path = path, info = info, solution = solution, law = law, agree = "false")
    db.session.add(new_request)
    db.session.commit()
    return success_response(new_request.serialize(), 201)


@app.route("/api/request/<int:id>/", methods=['GET'])
def get_situation_request(id):
    request = Request.query.filter_by(id = id).first()
    if request is None:
        return failure_response("Request not found!")
    return success_response(request.serialize(), 201)


@app.route("/api/users/receive/", methods=['POST'])
def receive_request():
    body = json.loads(request.data)
    request_id = body.get("request_id")
    accepted = body.get("accepted")
    tag_id = body.get("tag_id")

    r = Request.query.filter_by(id = request_id).first()
    t = Tag.query.filter_by(id = tag_id).first()
    
    if r is None or t is None:
        return failure_response("Incomplete field!")
    if accepted not in ("true", "false"):
        return failure_response("Invalid field!")

    path = r.path 
    info = r.info
    solution = r.solution 
    law = r.law 

    if accepted == "true":
        r.accepted = "true"
        the_situation = Situation.query.filter_by(path = path).first()
        if the_situation is not None:
            the_situation.info = info
            if solution is not None:
              the_situation.solution = solution
            if law is not None:
              the_situation.law = law
            db.session.commit()
            return success_response(the_situation.serialize(), 201)
        else:
            new_situation = Situation(path = path, info = info, solution = solution, law = law)       
                    
            db.session.add(new_situation)
            t.situation.append(new_situation)
            new_situation.tag.append(t)
            db.session.commit()
            return success_response(new_situation.serialize(), 201)




if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
