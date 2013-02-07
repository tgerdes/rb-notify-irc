from django.contrib import admin
from reviewboard.extensions.base import get_extension_manager

from rbnotifyirc.extension import RbNotifyIrc
from rbnotifyirc.models import IrcConfiguration, RepositoryNotification


# You must get the loaded instance of the extension to register to the
# admin site.
extension_manager = get_extension_manager()
extension = extension_manager.get_enabled_extension(RbNotifyIrc.id)


class RepositoryNotificationAdmin(admin.ModelAdmin):
    list_display = ('repository', 'irc_configuration')
    search_fields = ('repository__name',)

# Register the Model to the sample_extensions admin site.
extension.admin_site.register(IrcConfiguration)
extension.admin_site.register(RepositoryNotification,
                              RepositoryNotificationAdmin)

