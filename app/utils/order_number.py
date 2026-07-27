from datetime import datetime
from uuid import uuid4


def generate_order_number() -> str:
    """
    Generates a unique order number.

    Example:
    ORD-20260727-8F3A1C7D
    """
    return (
        f"ORD-"
        f"{datetime.now().strftime('%Y%m%d')}-"
        f"{uuid4().hex[:8].upper()}"
    )
