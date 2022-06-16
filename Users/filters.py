import django_filters
from .models import CustomUser


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'nationality_id',
                  'is_superuser', 'is_staff', 'is_active',)

        # occupation salary date joined
