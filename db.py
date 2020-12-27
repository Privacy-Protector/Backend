from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

situation_tag = db.Table(
    "situation_tag",
    db.Model.metadata,
    db.Column("situation_id", db.Integer, db.ForeignKey("situation.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"))
)

situation_whitelist = db.Table(
    "situation_whitelist",
    db.Model.metadata,
    db.Column("situation_id", db.Integer, db.ForeignKey("situation.id")),
    db.Column("whitelist_id", db.Integer, db.ForeignKey("whitelist.id"))
)

class Situation(db.Model):
    __tablename__ = "situation"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
    case = db.Column(db.String)
    solution = db.Column(db.String)
    law = db.Column(db.String)
    
    tag = db.relationship("Tag", secondary=situation_tag, back_populates="situation")
    whitelist = db.relationship("Whitelist", secondary=situation_whitelist, back_populates="situation")

    def __init__(self, **kwargs):
        self.path = kwargs.get("path", "")
        self.info = kwargs.get("info", "")
        self.case = kwargs.get("case", "")
        self.solution = kwargs.get("solution", "")
        self.law = kwargs.get("law", "")
    
    def serialize(self):
        if self.law is None:
            return{
                "id": self.id,
                "path": self.path,
                "info": self.info,
                "case": self.case,
                "solution": self.solution,
                "tag": [s.serialize() for s in self.tag],
                "whitelist": [w.serialize() for w in self.whitelist]
            }
        else:
            return{
                "id": self.id,
                "path": self.path,
                "info": self.info,
                "case": self.case,
                "solution": self.solution,
                "law": self.law,
                "tag": [s.serialize() for s in self.tag],
                "whitelist": [w.serialize() for w in self.whitelist]
            }
  
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    situation = db.relationship("Situation", secondary=situation_tag, back_populates="tag")
    
    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "")
    
    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
        }

class Whitelist(db.Model):
    __tablename__ = "whitelist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    situation = db.relationship("Situation", secondary=situation_whitelist, back_populates="whitelist")
    
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
        }

class Request(db.Model):
    __tablename__ = "request"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
    case = db.Column(db.String)
    solution = db.Column(db.String)
    law = db.Column(db.String)
    agree = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.path = kwargs.get("path", "")
        self.info = kwargs.get("info", "")
        self.case = kwargs.get("case", "")
        self.solution = kwargs.get("solution", "")
        self.law = kwargs.get("law", "")
        self.agree = kwargs.get("agree", "")

    def serialize(self):
        if self.law is None:
          return{
              "id": self.id,
              "path": self.path,
              "info": self.info,
              "case": self.case,
              "solution": self.solution,
              "agree": self.agree
          }
        else:
          return{
              "id": self.id,
              "path": self.path,
              "info": self.info,
              "case": self.case,
              "solution": self.solution,
              "law": self.law,
              "agree": self.agree
          }
