from app import router


class API:
    def __init__(self, *args):
        for route in args:
            router.include_router(route.ep)

            if hasattr(route, "legacy_ep"):
                router.include_router(route.legacy_ep)
