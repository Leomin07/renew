from app.core.config import setting


async def common_params(
    pageSize: int = 10, pageIndex: int = 1, search: str | None = None
):
    return {"pageSize": pageSize, "pageIndex": pageIndex, "search": search}


def generate_key(user_id: int, end_point: str | None = None):
    return f"{setting.APP_NAME}_USER_ID:{user_id}_{end_point}"
