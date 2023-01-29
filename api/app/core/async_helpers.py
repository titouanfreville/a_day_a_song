class Asyncrange:
    class __Asyncrange:
        def __init__(self, *args):
            self.__iter_range = iter(range(*args))

        async def __anext__(self):
            try:
                return next(self.__iter_range)
            except StopIteration as e:
                raise StopAsyncIteration(str(e))

    def __init__(self, *args):
        self.__args = args

    def __aiter__(self) -> __Asyncrange:
        return self.__Asyncrange(*self.__args)
