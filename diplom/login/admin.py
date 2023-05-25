from django.contrib import admin

from .models import Income, Spending, Account, Saving

admin.site.register(Income)
admin.site.register(Spending)
admin.site.register(Account)
admin.site.register(Saving)
