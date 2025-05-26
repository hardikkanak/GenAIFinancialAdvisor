from django.contrib import admin
from .models import AdviceHistory
from django.utils.html import format_html
from django.utils.text import Truncator

@admin.register(AdviceHistory)
class AdviceHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_advice', 'similar_profiles_percentage', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__email', 'advice_html')

    def short_advice(self, obj):
        return Truncator(obj.advice_html).chars(100)
    short_advice.short_description = "Advice Preview"