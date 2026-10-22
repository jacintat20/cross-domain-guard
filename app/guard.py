from enum import IntEnum
from typing import Optional

class Classification(IntEnum):
    UNCLASS = 1
    SECRET = 2

class GuardPolicyEngine:
    @staticmethod
    def validate_clearance(user_clearance: str, message_label: str) -> bool:
        """Enforces that user clearance level meets or exceeds message classification."""
        try:
            user_level = Classification[user_clearance.upper()]
            msg_level = Classification[message_label.upper()]
            return user_level >= msg_level
        except KeyError:
            return False
    
    @staticmethod
    def validate_flow(source_level: str, dest_level: str) -> bool:
        """Enforces one-way flow: Low-to-High allowed, High-to-Low blocked."""
        try:
            src = Classification[source_level.upper()]
            dst = Classification[dest_level.upper()]
            # high-to-low leakeage prevention
            return src <= dst
        except KeyError:
            return False