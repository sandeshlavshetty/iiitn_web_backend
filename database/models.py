from flask_sqlalchemy import SQLAlchemy
from database import db

db = SQLAlchemy() 

# person table




# media tables


class MediaImageCard(db.Model):
    __tablename__ = "media_image_card"
    media_img_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_file_name = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.Text, nullable=False)

class MediaVideoCard(db.Model):
    __tablename__ = "media_video_card"
    media_vid_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_file_name = db.Column(db.String(255), nullable=False)
    video_path = db.Column(db.Text, nullable=False)

class MediaDocCard(db.Model):
    __tablename__ = "media_doc_card"
    media_doc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doc_file_name = db.Column(db.String(255), nullable=False)
    doc_path = db.Column(db.Text, nullable=False)


