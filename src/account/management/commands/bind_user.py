from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand

from ...models import Seller


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, crated = Group.objects.get_or_create(
            name="Sellers"
        )
        permission_change_sellerproduct, created = Permission.objects.get_or_create(
            codename="change_sellerproduct"
        )
        permission_add_sellerproduct, created = Permission.objects.get_or_create(
            codename="add_sellerproduct"
        )
        group.permissions.add(permission_change_sellerproduct)
        group.permissions.add(permission_add_sellerproduct)
        group.save()

        for seller in Seller.objects.all():
            seller.profile.groups.add(group)
            seller.profile.is_staff = True
            seller.profile.save()
