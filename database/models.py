from flask_sqlalchemy import SQLAlchemy
from database import db
from datetime import datetime
from sqlalchemy import CheckConstraint, Enum








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
    
# Media 
class Media(db.Model):
    __tablename__ = 'media'
    m_id = db.Column(db.Integer, primary_key=True)
    m_category = db.Column(db.String(50), nullable=False)
    m_sub_category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('person.p_id'))
    updated_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey('person.p_id'))
    added_time = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    media_img_id = db.Column(db.Integer, db.ForeignKey('media_image_card.media_img_id', ondelete='SET NULL'))
    media_vid_id = db.Column(db.Integer, db.ForeignKey('media_video_card.media_vid_id', ondelete='SET NULL'))
    media_doc_id = db.Column(db.Integer, db.ForeignKey('media_doc_card.media_doc_id', ondelete='SET NULL'))



class Card(db.Model):
    __tablename__ = "card"
    
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_category = db.Column(db.String(100))
    c_sub_category = db.Column(db.String(100))
    title = db.Column(db.String(255))
    caption = db.Column(db.Text)
    content = db.Column(db.Text)
    date = db.Column(db.Date)
    location = db.Column(db.String(255))
    media_img_id = db.Column(db.Integer, db.ForeignKey("media_image_card.media_img_id", ondelete="SET NULL"))
    media_vid_id = db.Column(db.Integer, db.ForeignKey("media_video_card.media_vid_id", ondelete="SET NULL"))
    media_doc_id = db.Column(db.Integer, db.ForeignKey("media_doc_card.media_doc_id", ondelete="SET NULL"))
    updated_by = db.Column(db.Integer, db.ForeignKey("person.p_id"))
    updated_time = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey("person.p_id"))
    added_time = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    # New column for visibility (default is True)
    visibility = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self):
        """Convert Card object to dictionary format for JSON responses."""
        return {
            "c_id": self.c_id,
            "c_category": self.c_category,
            "c_sub_category": self.c_sub_category,
            "title": self.title,
            "caption": self.caption,
            "content": self.content,
            "date": self.date.strftime('%Y-%m-%d') if self.date else None,
            "location": self.location,
            "media_img_id": self.media_img_id,
            "media_vid_id": self.media_vid_id,
            "media_doc_id": self.media_doc_id,
            "updated_by": self.updated_by,
            "updated_time": self.updated_time.strftime('%Y-%m-%d %H:%M:%S') if self.updated_time else None,
            "added_by": self.added_by,
            "added_time": self.added_time.strftime('%Y-%m-%d %H:%M:%S') if self.added_time else None,
            "visibility": self.visibility
        }

    
    

# Department Table
class Department(db.Model):
    __tablename__ = "department"
    d_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dept_name = db.Column(db.String(100), nullable=False)
    branch_name = db.Column(db.String(100), nullable=False)
    

# Many-to-Many Association Table (FacultyStaff <-> Publication)
faculty_publication = db.Table(
    "faculty_publication",
    db.Column("f_id", db.Integer, db.ForeignKey("faculty_staff.f_id", ondelete="CASCADE"), primary_key=True),
    db.Column("pub_id", db.Integer, db.ForeignKey("publication.pub_id", ondelete="CASCADE"), primary_key=True)
)
    
    
class FacultyStaff(db.Model):
    __tablename__ = "faculty_staff"

    f_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    p_id = db.Column(db.Integer, db.ForeignKey("person.p_id", ondelete="CASCADE"), unique=True)
    join_year = db.Column(db.Integer, nullable=False)
    media_img_id = db.Column(db.Integer, db.ForeignKey("media_image_card.media_img_id", ondelete="SET NULL"))
    d_id = db.Column(db.Integer, db.ForeignKey("department.d_id", ondelete="CASCADE"))
    positions = db.Column(db.Text, nullable=False)
    f_or_s = db.Column(db.Enum("Faculty", "Staff", name="ForS"), nullable=False)

    education = db.Column(db.Text)
    experience = db.Column(db.Text)
    teaching = db.Column(db.Text)
    research = db.Column(db.Text)

    # Relationships
    person = db.relationship("Person", backref="faculty_staff", uselist=False)
    department = db.relationship("Department", backref="department_faculty_staff")
    profile_image = db.relationship("MediaImageCard", backref="media_faculty_staff", uselist=False)
    publications = db.relationship("Publication", secondary=faculty_publication, back_populates="faculty_members")

    def to_dict(self):
        return {
            "f_id": self.f_id,
            "p_id": self.p_id,
            "join_year": self.join_year,
            "media_img_id": self.media_img_id,
            "d_id": self.d_id,
            "positions": self.positions,
            "f_or_s": self.f_or_s,
            "education": self.education,
            "experience": self.experience,
            "teaching": self.teaching,
            "research": self.research,
            "publications": [pub.to_dict() for pub in self.publications],
        }




class Student(db.Model):
    __tablename__ = "student"
    s_id = db.Column(db.String(20), primary_key=True)  # BT ID
    p_id = db.Column(db.Integer, db.ForeignKey("person.p_id", ondelete="CASCADE"), unique=True)
    join_year = db.Column(db.Integer, nullable=False)
    media_img_id = db.Column(db.Integer, db.ForeignKey("media_image_card.media_img_id", ondelete="SET NULL"))
    d_id = db.Column(db.Integer, db.ForeignKey("department.d_id", ondelete="CASCADE"))

    person = db.relationship("Person", backref="student", uselist=False)
    department = db.relationship("Department", backref="students")
    profile_image = db.relationship("MediaImageCard", backref="student", uselist=False)
    
    

class Publication(db.Model):
    __tablename__ = "publication"

    pub_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False)
    type = db.Column(db.Text, nullable=False)
    
    # Updated branch to ENUM
    branch = db.Column(Enum("CSE", "ECE", "BS", name="branch_enum"), nullable=False)

    # New attributes
    lead_name = db.Column(db.String(255), nullable=True)
    published_in = db.Column(db.String(255), nullable=True)

    faculty_members = db.relationship("FacultyStaff", secondary=faculty_publication, back_populates="publications")

    __table_args__ = (
        CheckConstraint("status IN ('ongoing', 'completed', 'proposed')", name="check_publication_status"),
    )

    def to_dict(self):
        return {
            "pub_id": self.pub_id,
            "title": self.title,
            "content": self.content,
            "link": self.link,
            "status": self.status,
            "type": self.type,
            "branch": self.branch,
            "lead_name": self.lead_name,
            "published_in": self.published_in,
        }


class Alumni(db.Model):
    __tablename__ = 'alumni'

    s_id = db.Column(db.String(20), db.ForeignKey('student.s_id'), primary_key=True)
    curr_org = db.Column(db.String(255), nullable=True)
    brief = db.Column(db.Text, nullable=True)

    student = db.relationship('Student', backref=db.backref('alumni', uselist=False))
