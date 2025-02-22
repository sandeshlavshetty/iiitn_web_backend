from database import db
from database.models import MediaImageCard, MediaVideoCard, MediaDocCard, SocialMedia, Media
from flask import current_app



# for media uploads 
def add_media(file_name, file_path, media_type):
    """Add media entry to the respective table."""
    if media_type == "image":
        media = MediaImageCard(image_file_name=file_name, image_path=file_path)
    elif media_type == "video":
        media = MediaVideoCard(video_file_name=file_name, video_path=file_path)
    elif media_type == "doc":
        media = MediaDocCard(doc_file_name=file_name, doc_path=file_path)
    else:
        return None

    db.session.add(media)
    db.session.commit()
    return media

def get_media(media_type, media_id):
    """Fetch media details by ID."""
    if media_type == "image":
        return MediaImageCard.query.get(media_id)
    elif media_type == "video":
        return MediaVideoCard.query.get(media_id)
    elif media_type == "doc":
        return MediaDocCard.query.get(media_id)
    return None

def delete_media(media_type, media_id):
    """Delete media entry from DB."""
    media = get_media(media_type, media_id)
    if media:
        db.session.delete(media)
        db.session.commit()
        return True
    return False


# social media
def add_social_media(insta, twitter, linkedin, youtube):
    """Add or update social media links (only one row allowed)."""
    sm_entry = SocialMedia.query.first()

    if sm_entry:
        sm_entry.insta = insta
        sm_entry.twitter = twitter
        sm_entry.linkedin = linkedin
        sm_entry.youtube = youtube
    else:
        sm_entry = SocialMedia(insta=insta, twitter=twitter, linkedin=linkedin, youtube=youtube)
        db.session.add(sm_entry)

    db.session.commit()  
    return sm_entry  # ✅ Return the updated object


def get_social_media():
    """Fetch the stored social media links and ensure they are accessible."""
    sm_entry = SocialMedia.query.first()

    if sm_entry:
        db.session.refresh(sm_entry)  # ✅ Ensure attributes are accessible before returning
    return sm_entry


def delete_social_media():
    """Delete the only social media record."""
    sm_entry = SocialMedia.query.first()
    
    if sm_entry:
        db.session.refresh(sm_entry)  # ✅ Ensure it's active in the session
        db.session.delete(sm_entry)
        db.session.commit()
        return True
    
    return False


from database import db
from database.models import Person, SocialMedia
from werkzeug.security import generate_password_hash, check_password_hash

def add_person(email_pri, email_sec, name, phone_no, alt_phone_no, curr_address, perm_address, password, role, sm_id=None):
    """Add a new person."""
    hashed_password = generate_password_hash(password)
    person = Person(
        email_pri=email_pri,
        email_sec=email_sec,
        name=name,
        phone_no=phone_no,
        alt_phone_no=alt_phone_no,
        curr_address=curr_address,
        perm_address=perm_address,
        password=hashed_password,
        role=role,
        sm_id=sm_id
    )
    db.session.add(person)
    db.session.commit()
    return person

def get_person(p_id):
    """Fetch person details by ID."""
    return Person.query.get(p_id)

def get_all_persons():
    """Fetch all persons."""
    return Person.query.all()

def update_person(p_id, **kwargs):
    """Update person details."""
    person = Person.query.get(p_id)
    if not person:
        return None

    for key, value in kwargs.items():
        if key == "password":
            setattr(person, key, generate_password_hash(value))  # Hash new password
        elif hasattr(person, key):
            setattr(person, key, value)

    db.session.commit()
    return person

def delete_person(p_id):
    """Delete a person."""
    person = Person.query.get(p_id)
    if person:
        db.session.delete(person)
        db.session.commit()
        return True
    return False




def create_media(data):
    new_media = Media(
        m_category=data.get('m_category'),
        m_sub_category=data.get('m_sub_category'),
        title=data.get('title'),
        updated_by=data.get('updated_by'),
        added_by=data.get('added_by'),
        media_img_id=data.get('media_img_id'),
        media_vid_id=data.get('media_vid_id'),
        media_doc_id=data.get('media_doc_id')
    )
    db.session.add(new_media)
    db.session.commit()
    return new_media

def get_all_media():
    return Media.query.all()

def get_media_by_id(m_id):
    return Media.query.get(m_id)

def update_media(m_id, data):
    media = Media.query.get(m_id)
    if not media:
        return None
    media.M_category = data.get('m_category', media.m_category)
    media.M_sub_category = data.get('m_sub_category', media.m_sub_category)
    media.Title = data.get('title', media.Title)
    media.Updated_by = data.get('updated_by', media.Updated_by)
    media.media_img_id = data.get('media_img_id', media.media_img_id)
    media.media_vid_id = data.get('media_vid_id', media.media_vid_id)
    media.media_doc_id = data.get('media_doc_id', media.media_doc_id)
    db.session.commit()
    return media

def delete_media(m_id):
    media = Media.query.get(m_id)
    if not media:
        return False
    db.session.delete(media)
    db.session.commit()
    return True
