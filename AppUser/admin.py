from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    
    # Fields shown in list view
    list_display = ('username', 'email', 'college_name', 'is_staff')

    # Add your custom fields in admin form
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("college_name", "skills", "portfolio_link", "current_resume","resume_raw_text","current_skills_projects")
        }),
    )

    # Fields when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "fields": ("college_name", "skills", "portfolio_link", "current_resume","resume_raw_text","current_skills_projects")
        }),
    )


admin.site.register(User, CustomUserAdmin)

# Register your models here.
