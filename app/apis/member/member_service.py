from app.db.models import member_model
from sqlalchemy.orm import Session


def get_profile(db: Session, member_id: int):
    member = db.query(member_model.Member).filter_by(id=member_id).first()

    return member
