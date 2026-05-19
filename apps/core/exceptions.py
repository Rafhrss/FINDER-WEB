from django.core.exceptions import PermissionDenied, ValidationError


class CampusEmailValidationError(ValidationError):
    pass


class OwnershipValidationError(PermissionDenied):
    pass


class ChatParticipantValidationError(PermissionDenied):
    pass


class ChatReadOnlyError(PermissionDenied):
    pass
