from enum import Enum


class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    END_TO_END = "end_to_end"
