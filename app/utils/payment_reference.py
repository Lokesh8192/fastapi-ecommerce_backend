from datetime import datetime
from uuid import uuid4


def generate_payment_reference() -> str:
    return (
        f"PAY-"
        f"{datetime.now().strftime('%Y%m%d')}-"
        f"{uuid4().hex[:8].upper()}"
    )
