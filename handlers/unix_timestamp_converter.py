from datetime import datetime


class TimestampConverter:
    @staticmethod
    def to_timestamp(date_input: datetime) -> int:
        if isinstance(date_input, datetime):
            dt = date_input
        else:
            raise TypeError("Input must be a datetime object")
        return int(dt.timestamp())

    @staticmethod
    def to_human_date(date_input: int, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        if isinstance(date_input, int):
            dt = datetime.fromtimestamp(date_input)
            return dt.strftime(format_str)
        else:
            raise TypeError("Input must be a timestamp (int)")
