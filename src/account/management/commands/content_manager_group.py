from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name="Content-managers"
        )
        permission_view_profile, created = Permission.objects.get_or_create(
            codename="view_profile"
        )
        permission_add_seller, created = Permission.objects.get_or_create(
            codename="add_seller"
        )
        permission_change_seller, created = Permission.objects.get_or_create(
            codename="change_seller"
        )
        permission_delete_seller, created = Permission.objects.get_or_create(
            codename="delete_seller"
        )
        permission_add_category, created = Permission.objects.get_or_create(
            codename="add_category"
        )
        permission_change_category, created = Permission.objects.get_or_create(
            codename="change_category"
        )
        permission_delete_category, created = Permission.objects.get_or_create(
            codename="delete_category"
        )
        permission_add_product, created = Permission.objects.get_or_create(
            codename="add_product"
        )
        permission_change_product, created = Permission.objects.get_or_create(
            codename="change_product"
        )
        permission_delete_product, created = Permission.objects.get_or_create(
            codename="delete_product"
        )
        permission_add_sellerproduct, created = Permission.objects.get_or_create(
            codename="add_sellerproduct"
        )
        permission_change_sellerproduct, created = Permission.objects.get_or_create(
            codename="change_sellerproduct"
        )
        permission_delete_sellerproduct, created = Permission.objects.get_or_create(
            codename="delete_sellerproduct"
        )
        permission_add_picture, created = Permission.objects.get_or_create(
            codename="add_picture"
        )
        permission_change_picture, created = Permission.objects.get_or_create(
            codename="change_picture"
        )
        permission_delete_picture, created = Permission.objects.get_or_create(
            codename="delete_picture"
        )
        permission_delete_review, created = Permission.objects.get_or_create(
            codename="delete_review"
        )

        group.permissions.add(permission_view_profile)
        group.permissions.add(permission_add_seller)
        group.permissions.add(permission_change_seller)
        group.permissions.add(permission_delete_seller)
        group.permissions.add(permission_add_category)
        group.permissions.add(permission_change_category)
        group.permissions.add(permission_delete_category)
        group.permissions.add(permission_add_product)
        group.permissions.add(permission_change_product)
        group.permissions.add(permission_delete_product)
        group.permissions.add(permission_add_sellerproduct)
        group.permissions.add(permission_change_sellerproduct)
        group.permissions.add(permission_delete_sellerproduct)
        group.permissions.add(permission_add_picture)
        group.permissions.add(permission_change_picture)
        group.permissions.add(permission_delete_picture)
        group.permissions.add(permission_delete_review)
        group.save()
