from database import db
from database.models import MediaImageCard, MediaVideoCard, MediaDocCard, SocialMedia, Media, Card
from flask import current_app
from utils.file_helper import delete_file



# these are for img,vdeo,doc media uploads 



def add_media(file_name, file_path):
    """Add media entry to the respective table."""
    file_ext = file_name.split('.')[-1].lower()
    if file_ext in ["jpg", "jpeg", "png", "gif", "webp"]:
        media = MediaImageCard(image_file_name=file_name, image_path=file_path)
    elif file_ext in ["mp4", "mov", "avi", "mkv"]:
        media = MediaVideoCard(video_file_name=file_name, video_path=file_path)
    elif file_ext in ["pdf", "doc", "docx", "txt"]:
         media = MediaDocCard(doc_file_name=file_name, doc_path=file_path)
    else:
        return None

    db.session.add(media)
    db.session.commit()
    return media

# def get_media(media_type, media_id):
#     """Fetch media details by ID."""
#     if media_type == "image":
#         return MediaImageCard.query.get(media_id)
#     elif media_type == "video":
#         if media_id:
#             return MediaVideoCard.query.get(media_id)
#     elif media_type == "doc":
#         if media_id:
#             return MediaDocCard.query.get(media_id)
#     return None

def get_media(media_id):
    """Fetch media details by ID from any media table."""
    media = MediaImageCard.query.get(media_id) or \
            MediaVideoCard.query.get(media_id) or \
            MediaDocCard.query.get(media_id)
    
    return media



def delete_media_type(media_id):
    media = get_media(media_id)
    if not media:
        return False  # Media does not exist in the database
    
    
    supa_delete = delete_file(media.image_path)
    if supa_delete == "supa delete error":  # Fixing check
        return False  # Prevent database deletion if Supabase deletion fails

    db.session.delete(media)
    db.session.commit()
    return True

def get_media_path(media_id, media_type):
    if media_type == "image":
        media = MediaImageCard.query.get(media_id)
        return media.image_path if media else None
    elif media_type == "video":
        media = MediaVideoCard.query.get(media_id)
        return media.video_path if media else None
    elif media_type == "doc":
        media = MediaDocCard.query.get(media_id)
        return media.doc_path if media else None
    else:
        return None



# this is for social media

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

#  this is for Person table

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


# these operations are for Media table 

def create_media(data):
    new_media = Media(
        m_category=data.get('m_category'),
        m_sub_category=data.get('m_sub_category'),
        title=data.get('title'),
        updated_by=data.get('updated_by'),
        added_by=data.get('added_by'),
        media_img_id=data.get('media_img_id'),
        media_vid_id=data.get('media_vid_id'),
        media_doc_id=data.get('media_doc_id'),
        preference=data.get('preference'),
        expiry_date=data.get('expiry_date'),
        date= data.get('date')
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
    media.preference=data.get('preference',media.preference)
    media.expiry_date=data.get('expiry_date',media.expiry_date)
    media.date= data.get('date',media.date)
    db.session.commit()
    return media

def delete_media(m_id):
    media = Media.query.get(m_id)
    
    if not media:
        return False
    db.session.delete(media)
    db.session.commit()
    return True

#these are for Card table

def add_card(session, card_data):
    card = Card(**card_data)
    session.add(card)
    session.commit()
    return card

def get_card_by_id(session, c_id):
    return session.query(Card).filter_by(c_id=c_id).first()

def update_card(session, c_id, card_data):
    card = session.query(Card).filter_by(c_id=c_id).first()
    if card:
        for key, value in card_data.items():
            setattr(card, key, value)
        session.commit()
    return card

def delete_card(session, c_id):
    card = session.query(Card).filter_by(c_id=c_id).first()
    if card:
        session.delete(card)
        session.commit()
    return card

