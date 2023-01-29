from pytest import mark, raises

from app.core.generators import Generate


class TestGenerators:
    class TestSingleTimeCode:
        def test_should_generate_code_with_correct_char_set(self):
            code, _ = Generate.one_time_unique_code("ab01", 20)

            assert len(code) == 20
            for char in code:
                if char not in ["a", "b", "0", "1"]:
                    raise AssertionError("Unexpected char", char)

        def test_should_return_correct_max_number_of_code_comb(self):
            _, nb_comb = Generate.one_time_unique_code("ab01", 2)

            assert nb_comb == 16

            _, nb_comb = Generate.one_time_unique_code("ab", 4)

            assert nb_comb == 16

            _, nb_comb = Generate.one_time_unique_code("ab01", 4)

            assert nb_comb == 256

    class TestMultipleCodeGeneration:
        @mark.asyncio
        async def test_should_be_able_to_generate_multiple_codes_from_function(self):
            res = await Generate.generate_multiple(10, Generate.one_time_unique_code)

            assert len(res) == 10
            assert len(set(res)) == 10

            res2 = await Generate.generate_multiple(70, Generate.one_time_unique_code)

            assert len(res2) == 70
            assert len(set(res2)) == 70

        @mark.asyncio
        async def test_should_raise_error_if_cannot_generate_enougth_code(self):
            def __single_fun():
                return "a", 1

            with raises(Generate.TooManyCodes):
                await Generate.generate_multiple(2, __single_fun)

            with raises(Generate.TooManyCodes):
                await Generate.generate_multiple(17, Generate.one_time_unique_code, "ab", 4)
            with raises(Generate.TooManyCodes):
                await Generate.generate_multiple(
                    3, Generate.one_time_unique_code, "ab", 2, existing_codes={"ab", "aa"}
                )

        @mark.asyncio
        async def test_should_return_unique_new_data_only(self):
            for _ in range(0, 1000):
                res = await Generate.generate_multiple(
                    2, Generate.one_time_unique_code, "ab", 2, existing_codes={"ab", "aa"}
                )

                assert len(res) == 2
                assert "ab" not in res
                assert "aa" not in res
