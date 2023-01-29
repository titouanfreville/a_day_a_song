from datetime import datetime
from zoneinfo import ZoneInfo

from app.core import time
from pytest import raises


class TestTimeFeatures:
    class TestConvetions:
        def test_should_correctly_converts_millisecondes_to_seconds(self):
            assert time.Converts.milli_to_seconds(1000) == 1, "Invalid convertion to milliseconds"
            assert (
                time.Converts.milli_to_seconds(10000) == 10
            ), "Invalid convertion to milliseconds"
            assert time.Converts.milli_to_seconds(100) == 0, "Should not keep under seconds value"
            assert time.Converts.milli_to_seconds(999) == 0, "Should not keep under seconds value"
            assert time.Converts.milli_to_seconds(1999) == 1, "Should not keep under seconds value"

        class TestTimezones:
            def test_should_correctly_converts_unaware_datetime_to_utc(self):
                dt = datetime.utcnow()
                assert time.Utils.is_naive(dt), "Datetime is not naïve"

                utc_dt = time.Converts.to_utc(dt)
                assert not time.Utils.is_naive(utc_dt), "Datetime is still naïve"
                assert utc_dt.tzinfo == ZoneInfo("UTC"), "Datetime is not utc"

            def test_should_correctly_converts_awsare_datetime_to_utc(self):
                dt = datetime.fromisoformat("2022-01-10T01:12:00+05:00")
                assert not time.Utils.is_naive(dt), "Datetime is not naïve"
                assert dt.tzinfo != ZoneInfo("UTC"), "Datetime is  utc"

                utc_dt = time.Converts.to_utc(dt)
                assert not time.Utils.is_naive(utc_dt), "Datetime became naïve"
                assert utc_dt.tzinfo == ZoneInfo("UTC"), "Datetime is not utc"
                assert utc_dt.isoformat() == "2022-01-09T20:12:00+00:00"
                assert (dt - utc_dt).total_seconds() == 0

                dt = datetime.utcnow().astimezone(ZoneInfo("Asia/Ho_Chi_Minh"))
                assert not time.Utils.is_naive(dt), "Datetime is naïve"
                assert dt.tzinfo != ZoneInfo("UTC"), "Datetime is  utc"

                utc_dt = time.Converts.to_utc(dt)
                assert not time.Utils.is_naive(utc_dt), "Datetime became naïve"
                assert utc_dt.tzinfo == ZoneInfo("UTC"), "Datetime is not utc"
                assert (dt - utc_dt).total_seconds() == 0
                if dt.hour > 7 and utc_dt.hour < 17:
                    assert dt.hour - utc_dt.hour == 7

            def test_should_correctly_convers_unaware_datetime_to_timezone(self):
                aimed_timezone = ZoneInfo("Asia/Ho_Chi_Minh")
                dt = datetime.utcnow()
                assert time.Utils.is_naive(dt), "Datetime is not naïve"

                localized = time.Converts.to_timezone(dt, aimed_timezone)
                assert not time.Utils.is_naive(localized), "Datetime is still naïve"
                assert localized.tzinfo == aimed_timezone, "Datetime is not utc"
                assert dt.hour != localized.hour
                with raises(TypeError):
                    (dt - localized).total_seconds()

                if localized.hour > 7 and dt.hour < 17:
                    assert localized.hour - dt.hour == 7

            def test_should_correctly_converts_awsare_datetime_to_other_timezone(self):
                aimed_timezone = ZoneInfo("Asia/Ho_Chi_Minh")

                dt = datetime.fromisoformat("2022-01-10T01:12:00+05:00")
                assert not time.Utils.is_naive(dt), "Datetime is naïve"
                assert dt.tzinfo != ZoneInfo("UTC"), "Datetime is  utc"

                localized = time.Converts.to_timezone(dt, aimed_timezone)
                assert not time.Utils.is_naive(localized), "Datetime became naïve"
                assert localized.tzinfo == aimed_timezone, "Datetime is not utc"
                assert localized.isoformat() == "2022-01-10T03:12:00+07:00"
                assert (dt - localized).total_seconds() == 0
                assert dt.hour != localized.hour
                if localized.hour > 2 and dt.hour < 22:
                    assert localized.hour - dt.hour == 2

                dt = datetime.utcnow().astimezone(ZoneInfo("America/Sao_Paulo"))
                assert not time.Utils.is_naive(dt), "Datetime is naïve"

                localized = time.Converts.to_timezone(dt, aimed_timezone)
                assert not time.Utils.is_naive(localized), "Datetime is still naïve"
                assert localized.tzinfo == aimed_timezone, "Datetime is not utc"
                assert dt.hour != localized.hour
                assert (dt - localized).total_seconds() == 0
