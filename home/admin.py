from django.contrib import admin
from home.models import Setting, ContactMessage, FAQ

class SettingAdmin(admin.ModelAdmin):
	list_display = ['title', 'company', 'updated_at', 'status']

class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ['name', 'subject', 'updated_at', 'status']
	readonly_fields = ('name', 'email', 'subject', 'message', 'ip')
	list_filter = ['status']

class FAQAdmin(admin.ModelAdmin):
	list_display = ['ordernumber', 'question', 'answer', 'status']
	list_filter = ['status']
		

admin.site.register(FAQ, FAQAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
