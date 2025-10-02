# Import all the models, so that Base has them before being imported by Alembic.
# # noqa: F401 (No Quality Assurance) for the linter.

from app.Core.Domain.Models.attachment import Attachment  # noqa: F401
from app.Core.Domain.Models.issue import Issue  # noqa: F401
from app.Core.Domain.Models.comment import Comment # noqa: F401
from app.Core.Domain.Models.notification import Notification # noqa: F401
from app.Core.Domain.Models.project import Project # noqa: F401
from app.Core.Domain.Models.user import User # noqa: F401
