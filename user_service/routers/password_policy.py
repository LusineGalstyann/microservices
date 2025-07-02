from typing import Tuple
import re

class PasswordPolicy:
    MIN_LENGTH = 8
    REQUIRE_UPPER = True
    REQUIRE_LOWER = True
    REQUIRE_DIGIT = True
    REQUIRE_SPECIAL = True
    SPECIAL_CHARACTERS = r"!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?"

def validate_password_complexity(password: str) -> Tuple[bool, str]:
    if len(password) < PasswordPolicy.MIN_LENGTH:
        return False, f"Password must be at least {PasswordPolicy.MIN_LENGTH} characters long."

    if PasswordPolicy.REQUIRE_UPPER and not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if PasswordPolicy.REQUIRE_LOWER and not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if PasswordPolicy.REQUIRE_DIGIT and not re.search(r"\d", password):
        return False, "Password must contain at least one digit."

    if PasswordPolicy.REQUIRE_SPECIAL and not re.search(f"[{re.escape(PasswordPolicy.SPECIAL_CHARACTERS)}]", password):
        return False, f"Password must contain at least one special character ({PasswordPolicy.SPECIAL_CHARACTERS})."

    return True, "Password is valid."
