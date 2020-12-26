from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table_1 = db.Table(
    "situation_tag",
    db.Model.metadata,
    db.Column("situation_id", db.Integer, db.ForeignKey("situation.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"))
)

class Situation(db.Model):
    __tablename__ = "situation"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
    solution = db.Column(db.String, nullable=False)
    law = db.Column(db.String)
    tag = db.relationship("Tag", secondary=association_table_1, back_populates="situation")

    def __init__(self, **kwargs):
        self.path = kwargs.get("path", "")
        self.info = kwargs.get("info", "")
        self.solution = kwargs.get("solution", "")
        self.law = kwargs.get("law", "")

    
    def serialize(self):
        if law is null:
          return{
              "id": self.id,
              "path": self.path,
              "info": self.info,
              "solution": self.solution,
              "tag": [s.serialize() for s in self.tag]
          }
        else:
          return{
              "id": self.id,
              "path": self.path,
              "info": self.info,
              "solution": self.solution
              "law": self.law,
              "tag": [s.serialize() for s in self.tag]
          }
  
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    situation = db.relationship("Situation", secondary=association_table_1, back_populates="tag")
    
    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "")
    
    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
        }

class Request(db.Model):
    __tablename__ = "request"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
    solution = db.Column(db.String)
    law = db.Column(db.String)
    agree = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.path = kwargs.get("path", "")
        self.info = kwargs.get("info", "")
        self.solution = kwargs.get("solution", "")
        self.law = kwargs.get("law", "")
        self.agree = kwargs.get("agree", "")

    def serialize(self):
        if law is null:
          return{
              "id": self.id,
              "path": self.path,
              "info": self.info,
              "solution": self.solution,
              "agree": self.agree
          }
        else:
          return{
              "id": self.id,
              "path": self.path,
              "info": self.info,
              "solution": self.solution
              "law": self.law,
              "agree": self.agree
          }
