from enum import Enum

class IssueType(Enum):
    BUG = "bug"
    FEATURE = "feature"
    TASK = "task"
    SECURITY = "security"
    
class IssueTypeStr(str, Enum):
    BUG = IssueType.BUG.value
    FEATURE = IssueType.FEATURE.value
    TASK = IssueType.TASK.value
    SECURITY = IssueType.SECURITY.value