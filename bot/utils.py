from datetime import timedelta


def validate_age(age: str) -> int | None:
    if not age.isdigit() or int(age) > 100:
        return None
    return int(age)


def convert_time_delta(date: timedelta) -> str:
    if date.total_seconds() < 0:
        return '0s'

    days, remainder = divmod(date.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    time_str = (
        f'{int(days)}d ' if days else ''
    ) + (
        f'{int(hours)}h ' if hours or days else ''
    ) + (
        f'{int(minutes)}m ' if minutes or hours or days else ''
    ) + f'{int(seconds)}s'

    return time_str
