from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db import IntegrityError

from authentication.models import Usuario


def admin_required(function=None, login_url='403'):
    return default_access(login_url=login_url, role_number=777, function=function, is_equal=True)


def access_basic_required(function=None, login_url='403'):
    return default_access(login_url=login_url, role_number=444, function=function)


def access_manager_required(function=None, login_url='403'):
    return default_access(login_url=login_url, role_number=755, function=function)


def default_access(login_url, role_number, function=None, redirect_field_name=REDIRECT_FIELD_NAME, is_equal=False):
    def verify_user_level(user):
        user_object = Usuario.objects.filter(user_id=user.pk).first()
        if user_object:
            if is_equal:
                return user.is_active and user_object.role == role_number
            else:
                return user.is_active and user_object.role >= role_number
        try:
            user_object = User.objects.get(pk=user.pk)
            return user_object.is_active and user_object.is_superuser
        except IntegrityError:
            pass

    actual_decorator = user_passes_test(
        verify_user_level,
        login_url=login_url, redirect_field_name=redirect_field_name
    )
    return actual_decorator(function) if function else actual_decorator
