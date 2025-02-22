from database import db
from database.models import MediaImageCard, MediaVideoCard, MediaDocCard

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

