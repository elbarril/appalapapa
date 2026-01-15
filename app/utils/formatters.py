"""
Formatting utilities for dates and prices.

All display formatting should use these functions for consistency.
All date formatting uses explicit Spanish names to ensure consistency across systems.
"""

from datetime import datetime
from typing import Union

from app.utils.constants import DATE_FORMAT_INPUT, SPANISH_DAYS, SPANISH_MONTHS


def format_date(date_input: Union[str, datetime, None], include_weekday: bool = True) -> str:
    """
    Format a date for display in Spanish.

    Args:
        date_input: Date as string (YYYY-MM-DD) or datetime object
        include_weekday: Whether to include the weekday name

    Returns:
        Formatted date string (e.g., "Lunes 15/01/2024")
    """
    if date_input is None:
        return ""

    if isinstance(date_input, str):
        try:
            date_obj = datetime.strptime(date_input, DATE_FORMAT_INPUT)
        except ValueError:
            return date_input  # Return as-is if parsing fails
    else:
        date_obj = date_input

    if include_weekday:
        weekday = SPANISH_DAYS[date_obj.weekday()]
        return f"{weekday} {date_obj.strftime('%d/%m/%Y')}"
    else:
        return date_obj.strftime("%d/%m/%Y")


def format_price(price: Union[float, int, str, None]) -> str:
    """
    Format a price for display with currency symbol.

    Args:
        price: Price as number or string

    Returns:
        Formatted price string (e.g., "$1,234.56")
    """
    if price is None:
        return "$0.00"

    try:
        numeric_price = float(price)
        return f"${numeric_price:,.2f}"
    except (ValueError, TypeError):
        return f"${price}"


def format_percentage(value: Union[float, int], decimal_places: int = 1) -> str:
    """
    Format a value as percentage.

    Args:
        value: Value to format (0-100 range)
        decimal_places: Number of decimal places

    Returns:
        Formatted percentage string (e.g., "75.5%")
    """
    try:
        return f"{float(value):.{decimal_places}f}%"
    except (ValueError, TypeError):
        return "0%"


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to specified length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append if truncated

    Returns:
        Truncated text with suffix if needed
    """
    if not text or len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def format_datetime(dt: Union[datetime, None]) -> str:
    """
    Format a datetime for display.

    Args:
        dt: Datetime object

    Returns:
        Formatted datetime string (e.g., "15/01/2024 14:30")
    """
    if dt is None:
        return ""

    return dt.strftime("%d/%m/%Y %H:%M")
