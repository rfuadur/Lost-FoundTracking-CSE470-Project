from datetime import datetime, timezone


def utc_now():
    """Naive UTC timestamp, replacing the deprecated datetime.utcnow().

    Returned value has no tzinfo so it stays comparable with existing
    naive-UTC timestamps already stored in the database.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)
