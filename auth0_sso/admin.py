from admin_tool_button.contrib.admin import ButtonActionAdmin
from auth0_sso.models import Auth0UserProfile, Auth0UserRole
from auth0_sso.roles import sync_roles
from django.contrib import admin, messages


class Auth0UserRoleAdmin(ButtonActionAdmin):

    button_actions = ['sync_roles']

    def has_add_permission(self, request):
        return False

    def sync_roles(self, request):
        if sync_roles():
            self.message_user(request,  'Roles synced', messages.SUCCESS)
        else:
            self.message_user(request, 'Error syncing roles', messages.ERROR)


admin.site.register(Auth0UserProfile)
admin.site.register(Auth0UserRole, Auth0UserRoleAdmin)
