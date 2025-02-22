from flask_sqlalchemy import SQLAlchemy
from database import db







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

#social media 

class SocialMedia(db.Model):
    __tablename__ = "social_media"
    sm_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    insta = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    youtube = db.Column(db.String(255))

# person table

class Person(db.Model):
    __tablename__ = "person"
    p_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_pri = db.Column(db.String(255), unique=True, nullable=False)
    email_sec = db.Column(db.String(255))
    name = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    alt_phone_no = db.Column(db.String(20))
    curr_address = db.Column(db.Text)
    perm_address = db.Column(db.Text)
    password = db.Column(db.String(255), nullable=False)  # Hashed password
    role = db.Column(db.String(50), nullable=False)
    sm_id = db.Column(db.Integer, db.ForeignKey("social_media.sm_id", ondelete="SET NULL"), unique=True)

    # Relationship
    social_media = db.relationship("SocialMedia", backref="person", uselist=False)
