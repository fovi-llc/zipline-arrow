import inspect
from functools import partial

import pandas as pd
from exchange_calendars import ExchangeCalendar as TradingCalendar
from exchange_calendars import clear_calendars
from exchange_calendars import get_calendar as ec_get_calendar  # get_calendar,
from exchange_calendars import (
    get_calendar_names,
    register_calendar,
    register_calendar_alias,
)
from exchange_calendars.calendar_utils import global_calendar_dispatcher

# from exchange_calendars.errors import InvalidCalendarName
from exchange_calendars.utils.pandas_utils import days_at_time  # noqa: reexport


# https://stackoverflow.com/questions/56753846/python-wrapping-function-with-signature
def wrap_with_signature(signature):
    def wrapper(func):
        func.__signature__ = signature
        return func

    return wrapper


@wrap_with_signature(inspect.signature(ec_get_calendar))
def get_calendar(*args, **kwargs):
    # We can't use the default ExchaneCalendar start which is 20 years before today when
    # ingesting or loading bundles that start before then.
    # There is the 1990-01-01 hack for four particular calendars but that doesn't work for others.
    # So when the user has an actual starting session date we use that minus 100 weeks
    # as a start date for the calendar in the case where the old behavior gives a too short calendar.
    start_session = kwargs.pop("start_session", None)
    kwargs.pop("end_session", None)

    if args[0] in ["us_futures", "CMES", "XNYS", "NYSE"]:
        calendar = ec_get_calendar(
            *args, side="right", start=pd.Timestamp("1990-01-01")
        )
    else:
        calendar = ec_get_calendar(*args, side="right")

    if start_session:
        min_calendar_start = start_session - pd.Timedelta(weeks=100)
        if calendar.first_session > min_calendar_start:
            calendar = ec_get_calendar(*args, side="right", start=min_calendar_start)

    return calendar


def get_calendar_for_bundle(bundle):
    return get_calendar(
        bundle.calendar_name,
        start_session=bundle.start_session,
        end_session=bundle.end_session,
    )


# get_calendar = compose(partial(get_calendar, side="right"), "XNYS")
# NOTE Sessions are now timezone-naive (previously UTC).
# Schedule columns now have timezone set as UTC
# (whilst the times have always been defined in terms of UTC,
# previously the dtype was timezone-naive).
