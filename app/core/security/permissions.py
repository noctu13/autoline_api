from app.domain.entities.user import User
from app.core.exceptions import PermissionsException


def check_admin(user: User):
    if not user.is_admin():
        raise PermissionsException