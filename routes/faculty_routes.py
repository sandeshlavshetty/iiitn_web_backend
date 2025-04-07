from flask import Blueprint, jsonify, request
from database.models import FacultyStaff, db, Person, Branch, MediaImageCard , Department, Publication,SocialMedia
from config import Config
import os


faculty_bp = Blueprint("faculty", __name__)
 
@faculty_bp.route("/", methods=["GET"])
def get_facultys():
    return jsonify({"message": "Faculty routes working!"})


@faculty_bp.route("/faculty_staff", methods=["GET"])
def get_faculty_staff():
    faculty_staff = (
        db.session.query(FacultyStaff, Person, Department, MediaImageCard)
        .join(Person, FacultyStaff.p_id == Person.p_id)
        .join(Department, FacultyStaff.d_id == Department.d_id)
        .outerjoin(MediaImageCard, FacultyStaff.media_img_id == MediaImageCard.media_img_id)  # Outer join to handle null images
        .all()
    )

    result = [
        {
            "f_id": faculty.f_id,
            "p_id": person.p_id,
            "name": person.name,
            "email": person.email_pri,
            "phone_no": person.phone_no,
            "join_year": faculty.join_year,
            "positions": faculty.positions,
            "f_or_s": faculty.f_or_s,
            "education": faculty.education,
            "experience": faculty.experience,
            "teaching": faculty.teaching,
            "research": faculty.research,
            "d_id": department.d_id,
            "dept_name": department.dept_name,
            "content": faculty.content,
            "preference": faculty.preference,
            "image_path": os.path.join(Config.SUPABASE_STORAGE_URL,media.image_path) if media else None
        }
        for faculty, person, department, media in faculty_staff
    ]

    return jsonify(result)

@faculty_bp.route("/faculty_staff/<int:f_id>", methods=["GET"])
def get_faculty_by_id(f_id):
    faculty_staff = (
        db.session.query(FacultyStaff, Person, Department, MediaImageCard)
        .join(Person, FacultyStaff.p_id == Person.p_id)
        .join(Department, FacultyStaff.d_id == Department.d_id)
        .outerjoin(MediaImageCard, FacultyStaff.media_img_id == MediaImageCard.media_img_id)
        .filter(FacultyStaff.f_id == f_id)
        .first()
    )

    if not faculty_staff:
        return jsonify({"message": "Faculty/Staff not found"}), 404

    faculty, person, department, media = faculty_staff

    return jsonify({
        "f_id": faculty.f_id,
        "p_id": person.p_id,
        "name": person.name,
        "email": person.email_pri,
        "phone_no": person.phone_no,
        "join_year": faculty.join_year,
        "positions": faculty.positions,
        "f_or_s": faculty.f_or_s,
        "education": faculty.education,
        "experience": faculty.experience,
        "teaching": faculty.teaching,
        "research": faculty.research,
        "d_id": department.d_id,
    "dept_name": department.dept_name,
        "content": faculty.content,
        "preference": faculty.preference,
        "image_path": os.path.join(Config.SUPABASE_STORAGE_URL,media.image_path) if media else None
    }), 200

@faculty_bp.route("/faculty_staff", methods=["POST"])
def create_faculty_staff():
    data = request.json
    new_faculty_staff = FacultyStaff(
        p_id=data["p_id"],
        join_year=data["join_year"],
        media_img_id=data.get("media_img_id"),
        d_id=data["d_id"],  # CHANGED from b_id to d_id
        positions=data["positions"],
        f_or_s=data["f_or_s"],
        education=data.get("education"),
        experience=data.get("experience"),
        teaching=data.get("teaching"),
        research=data.get("research"),
        content = data.get("content"),
        preference = data.get("preference")
    )

    db.session.add(new_faculty_staff)
    db.session.commit()
    return jsonify({"message": "Faculty/Staff created successfully"}), 201

@faculty_bp.route("/faculty_staff/<int:f_id>", methods=["PUT"])
def update_faculty_staff(f_id):
    data = request.json
    faculty_staff = FacultyStaff.query.get(f_id)

    if not faculty_staff:
        return jsonify({"message": "Faculty/Staff not found"}), 404

    faculty_staff.p_id = data.get("p_id", faculty_staff.p_id)
    faculty_staff.join_year = data.get("join_year", faculty_staff.join_year)
    faculty_staff.media_img_id = data.get("media_img_id", faculty_staff.media_img_id)
    faculty_staff.d_id = data.get("d_id", faculty_staff.d_id)  # CHANGED from b_id
    faculty_staff.positions = data.get("positions", faculty_staff.positions)
    faculty_staff.f_or_s = data.get("f_or_s", faculty_staff.f_or_s)
    faculty_staff.education = data.get("education", faculty_staff.education)
    faculty_staff.experience = data.get("experience", faculty_staff.experience)
    faculty_staff.teaching = data.get("teaching", faculty_staff.teaching)
    faculty_staff.research = data.get("research", faculty_staff.research)
    faculty_staff.preference = data.get("preference", faculty_staff.preference)

    db.session.commit()
    return jsonify({"message": "Faculty/Staff updated successfully"}), 200

@faculty_bp.route("/faculty_staff/<int:f_id>", methods=["DELETE"])
def delete_faculty_staff(f_id):
    faculty_staff = FacultyStaff.query.get(f_id)

    if not faculty_staff:
        return jsonify({"message": "Faculty/Staff not found"}), 404

    db.session.delete(faculty_staff)
    db.session.commit()
    return jsonify({"message": "Faculty/Staff deleted successfully"}), 200

@faculty_bp.route("/faculty_staff/<int:f_id>", methods=["PATCH"])
def patch_faculty_staff(f_id):
    data = request.json
    faculty_staff = FacultyStaff.query.get(f_id)

    if not faculty_staff:
        return jsonify({"message": "Faculty/Staff not found"}), 404

    # Update only the fields present in the request
    for key, value in data.items():
        if hasattr(faculty_staff, key):
            setattr(faculty_staff, key, value)

    db.session.commit()
    return jsonify({"message": "Faculty/Staff updated successfully"}), 200

@faculty_bp.route("/faculty_staff/default", methods=["PATCH"])
def create_default_faculty_staff():
    data = request.json

    # Create a new FacultyStaff entry with required fields and others set to None
    new_faculty_staff = FacultyStaff(
        p_id=data.get("p_id"),  # Required as it's unique and foreign key
        join_year=data.get("join_year", 2024),  # Default join year if not provided
        media_img_id=None,
        d_id=data.get("d_id"),  # CHANGED from b_id to d_id
        positions=data.get("positions", ""),  # Default to empty string
        f_or_s=data.get("f_or_s", "Faculty"),  # Defaulting to "Faculty"
        education=None,
        experience=None,
        teaching=None,
        research=None,
        content=None,
        preference=data.get("preference", 0)  # Default priority
    )

    db.session.add(new_faculty_staff)
    db.session.commit()

    return jsonify({
        "message": "Faculty/Staff created successfully",
        "faculty_staff": new_faculty_staff.to_dict()
    }), 201




@faculty_bp.route("/faculty_by_department/<int:d_id>", methods=["GET"])
def get_faculty_by_department(d_id):
    # Fetch faculty data by department
    faculty_staff = (
        db.session.query(FacultyStaff, Person, SocialMedia, Department, MediaImageCard, Publication)
        .join(Person, FacultyStaff.p_id == Person.p_id)
        .join(Department, FacultyStaff.d_id == Department.d_id)
        .outerjoin(SocialMedia, Person.sm_id == SocialMedia.sm_id)
        .outerjoin(MediaImageCard, FacultyStaff.media_img_id == MediaImageCard.media_img_id)  # Outer join to handle null images
        .join(Publication, FacultyStaff.f_id == Publication.f_id)  # Join with Publication
        .filter(Department.d_id == d_id)
        .order_by(FacultyStaff.preference.asc())  # Order by preference ascending
        .all()
    )

    grouped_publications = {}
    result = []

    for faculty, person, sm, department, media, publication in faculty_staff:
        # Group publications by type
        if publication.type not in grouped_publications:
            grouped_publications[publication.type] = []
        grouped_publications[publication.type].append({
            "pub_id": publication.pub_id,
            "title": publication.title,
            "content": publication.content,
            "status": publication.status,
            "type": publication.type,
            "branch": publication.branch_enum,
            "lead_name": publication.lead_name,
            "published_in": publication.published_in,
            "pub_year": publication.pub_year
        })

        # Prepare faculty data with their person and social media details
        faculty_data = {
            "f_id": faculty.f_id,
            "p_id": person.p_id,
            "name": person.name,
            "email": person.email_pri,
            "phone_no": person.phone_no,
            "join_year": faculty.join_year,
            "positions": faculty.positions,
            "f_or_s": faculty.f_or_s,
            "education": faculty.education,
            "experience": faculty.experience,
            "teaching": faculty.teaching,
            "research": faculty.research,
            "d_id": department.d_id,
            "dept_name": department.dept_name,
            "content": faculty.content,
            "preference": faculty.preference,
            "image_path": os.path.join(Config.MEDIA_BASE_URL, media.image_path) if media and media.image_path else None,
            "social_media": {
                "insta": sm.insta if sm else None,
                "twitter": sm.twitter if sm else None,
                "linkedin": sm.linkedin if sm else None,
                "youtube": sm.youtube if sm else None
            },
            "publications": grouped_publications
        }

        result.append(faculty_data)

    return jsonify(result)

#output format :- 
# {
#   "department": {
#     "d_id": 1,
#     "dept_name": "Computer Science Engineering",
#     "faculty": [
#       {
#         "f_id": 1,
#         "p_id": 101,
#         "name": "Dr. John Doe",
#         "email": "john.doe@example.com",
#         "phone_no": "+1234567890",
#         "join_year": 2015,
#         "positions": "Professor",
#         "f_or_s": "Faculty",
#         "education": "PhD in Computer Science",
#         "experience": "10 years",
#         "teaching": "Data Structures, Algorithms",
#         "research": "Machine Learning, AI",
#         "content": "Researcher in AI and Data Science",
#         "preference": 1,
#         "social_media": {
#           "insta": "john_doe_insta",
#           "twitter": "john_doe_twitter",
#           "linkedin": "john_doe_linkedin",
#           "youtube": "john_doe_youtube"
#         },
#         "publications": {
#           "publication": [
#             {
#               "pub_id": 101,
#               "title": "Deep Learning for AI",
#               "content": "In-depth research on deep learning algorithms",
#               "link": "https://example.com/deep-learning-ai",
#               "status": "completed",
#               "pub_year": 2020,
#               "lead_name": "Dr. John Doe",
#               "published_in": "AI Journal"
#             }
#           ],
#           "project": [
#             {
#               "pub_id": 102,
#               "title": "AI for Healthcare",
#               "content": "A research project on AI applications in healthcare",
#               "link": "https://example.com/ai-healthcare",
#               "status": "ongoing",
#               "pub_year": 2022,
#               "lead_name": "Dr. John Doe",
#               "published_in": "Tech Innovations"
#             }
#           ]
#         }
#       },
#       {
#         "f_id": 2,
#         "p_id": 102,
#         "name": "Prof. Alice Smith",
#         "email": "alice.smith@example.com",
#         "phone_no": "+0987654321",
#         "join_year": 2012,
#         "positions": "Associate Professor",
#         "f_or_s": "Faculty",
#         "education": "MSc in Computer Science",
#         "experience": "8 years",
#         "teaching": "Operating Systems, Networks",
#         "research": "Network Security",
#         "content": "Focuses on Cybersecurity and Network Defense",
#         "preference": 2,
#         "social_media": {
#           "insta": "alice_smith_insta",
#           "twitter": "alice_smith_twitter",
#           "linkedin": "alice_smith_linkedin",
#           "youtube": "alice_smith_youtube"
#         },
#         "publications": {
#           "publication": [
#             {
#               "pub_id": 103,
#               "title": "Secure Network Protocols",
#               "content": "A study on improving security protocols in networks",
#               "link": "https://example.com/secure-network-protocols",
#               "status": "completed",
#               "pub_year": 2018,
#               "lead_name": "Prof. Alice Smith",
#               "published_in": "Cybersecurity Journal"
#             }
#           ],
#           "consultancy": [
#             {
#               "pub_id": 104,
#               "title": "Network Security Consulting",
#               "content": "Providing consultation to tech firms on secure networks",
#               "link": "https://example.com/network-consulting",
#               "status": "completed",
#               "pub_year": 2021,
#               "lead_name": "Prof. Alice Smith",
#               "published_in": "Consultancy Magazine"
#             }
#           ]
#         }
#       }
#     ]
#   }
# }


# # Similar routes for other departments (just change the department id)
# @faculty_bp.route("/faculty_by_department/cse", methods=["GET"])
# def get_faculty_by_cse():
#     return get_faculty_by_department(d_id=1)  # Assuming CSE has d_id = 1

# @faculty_bp.route("/faculty_by_department/ece", methods=["GET"])
# def get_faculty_by_ece():
#     return get_faculty_by_department(d_id=2)  # Assuming ECE has d_id = 2

# @faculty_bp.route("/faculty_by_department/bs", methods=["GET"])
# def get_faculty_by_bs():
#     return get_faculty_by_department(d_id=3)  # Assuming BS has d_id = 3
