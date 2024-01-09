from app.core import config


async def common_params(
    pageSize: int = 10, pageIndex: int = 1, search: str | None = None
):
    return {"pageSize": pageSize, "pageIndex": pageIndex, "search": search}


def generate_key(member_id: int, end_point: str | None = None):
    return f"{config.APP_NAME}_MEMBER_ID:{member_id}_{end_point}"
