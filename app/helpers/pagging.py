from math import ceil


def return_paging(
    data: list, total_items: int, params: dict, metadata: dict | None = None
):
    totalPages = ceil(total_items / params["pageSize"])

    return {
        "paging": True,
        "hasMore": params["pageIndex"] < totalPages,
        "pageIndex": params["pageIndex"],
        "totalPages": ceil(total_items / params["pageSize"]),
        "total_items": total_items,
        "data": data,
        "metadata": metadata,
    }


def assign_paging(params: dict):
    params["pageIndex"] = int(params["pageIndex"])
    params["pageSize"] = int(params["pageSize"])
    params["skip"] = (params["pageIndex"] - 1) * params["pageSize"]
    return params
