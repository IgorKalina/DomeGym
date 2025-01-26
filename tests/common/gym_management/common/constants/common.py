import datetime
import uuid

NON_EXISTING_ID: uuid.UUID = uuid.UUID("a1111a11-12ca-4dd5-8f23-5f965a999aa9")

DEFAULT_DATETIME: datetime.datetime = datetime.datetime(2025, 2, 2, 0, 0, 0, 0, tzinfo=datetime.UTC)
NEW_UPDATED_AT: datetime.datetime = datetime.datetime(2025, 1, 1, 0, 0, 0, 0, tzinfo=datetime.UTC)
