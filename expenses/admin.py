from django.contrib import admin
from expenses.models import Accounts
from expenses.models import Expenses
from expenses.models import Income
from expenses.models import Category
from expenses.models import Subcategory
from expenses.models import Contractors
from expenses.models import Budget
# Register your models here.
admin.site.register(Accounts)
admin.site.register(Expenses)
admin.site.register(Income)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Contractors)
admin.site.register(Budget)