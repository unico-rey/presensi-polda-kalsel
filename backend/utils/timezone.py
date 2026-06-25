# backend/utils/timezone.py
"""Utility functions for handling timezone-aware datetime operations.

Provides a single helper ``now_wita`` that returns the current datetime in the
Asia/Makassar (WITA, UTC+7) timezone. Using ``zoneinfo`` ensures the tzinfo is
attached, avoiding naive datetime pitfalls throughout the codebase.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

WITA_TZ = ZoneInfo("Asia/Makassar")


def now_wita() -> datetime:
    """Return the current datetime localized to Asia/Makassar (UTC+7).

    The returned ``datetime`` is timezone‑aware (tzinfo set to ``WITA_TZ``) and
    can be used directly in comparisons, ``.date()`` calls, and when persisting
    to the database. SQLAlchemy will store the aware datetime correctly.
    """
    return datetime.now(tz=WITA_TZ)
