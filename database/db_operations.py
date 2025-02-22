from database import db
from database.models import MediaImageCard, MediaVideoCard, MediaDocCard
from database.models import SocialMedia
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

