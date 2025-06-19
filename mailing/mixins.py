from django.core.exceptions import PermissionDenied


class UserOrManagerViewAccessMixin:
    user_field = "user"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = getattr(obj, self.user_field, None)

        if user == self.request.user or self.request.user.is_staff:
            return obj
        raise PermissionDenied("У вас нет доступа к просмотру этого объекта.")


class UserOnlyEditMixin:
    user_field = "user"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = getattr(obj, self.user_field, None)

        if user == self.request.user:
            return obj
        raise PermissionDenied("Вы не можете изменить этот объект.")
