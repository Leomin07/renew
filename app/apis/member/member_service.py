import json
from loguru import logger
from app.core import config
from app.core.caching import get_cache, set_cache
from app.db.models import member_model
from sqlalchemy.orm import Session, load_only

from app.helpers.utils import generate_key


def get_profile(db: Session, member_id: int):
    endpoint = f"{config.APP_V1_STR}/member/me"
    key = generate_key(member_id, endpoint)

    data_cache = get_cache(key)
    if data_cache is not None:
        return json.loads(data_cache)

    member = (
        db.query(member_model.Member)
        .options(
            load_only(
                member_model.Member.id,
                member_model.Member.name,
                member_model.Member.username,
                member_model.Member.birthday,
                member_model.Member.phone,
                member_model.Member.status,
                member_model.Member.email,
                member_model.Member.gender,
            )
        )
        .filter_by(id=member_id)
        .first()
    )

    # ttl = 30 days = 2592000 seconds
    set_cache(key, json.dumps(member.dict()), 2592000)
    return member
