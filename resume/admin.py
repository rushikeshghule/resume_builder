from django.contrib import admin
from .models import (
    Resume, PersonalInfo, Education, WorkExperience, 
    Skill, Project, Certification, Language, Reference,
    ResumeTemplate
)

# Register your models here.
@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_dark_mode_supported', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_dark_mode_supported',)

class PersonalInfoInline(admin.StackedInline):
    model = PersonalInfo
    can_delete = False

class EducationInline(admin.TabularInline):
    model = Education
    extra = 0

class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 0

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0

class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 0

class LanguageInline(admin.TabularInline):
    model = Language
    extra = 0

class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 0

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'template', 'status', 'is_public', 'created_at', 'updated_at')
    list_filter = ('status', 'is_public', 'is_dark_mode', 'template')
    search_fields = ('title', 'user__username', 'user__email', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [
        PersonalInfoInline, EducationInline, WorkExperienceInline, 
        SkillInline, ProjectInline, CertificationInline, 
        LanguageInline, ReferenceInline
    ]

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'resume', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('resume__title',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'is_current')
    search_fields = ('institution', 'degree', 'field_of_study')
    list_filter = ('is_current', 'start_date', 'end_date')

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company', 'location', 'start_date', 'end_date', 'is_current')
    search_fields = ('job_title', 'company', 'location')
    list_filter = ('is_current', 'start_date', 'end_date')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'resume', 'order')
    search_fields = ('name',)
    list_filter = ('level',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'technologies', 'start_date', 'end_date', 'is_current', 'resume')
    search_fields = ('title', 'technologies', 'description')
    list_filter = ('is_current',)

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'date_obtained', 'expiration_date', 'resume')
    search_fields = ('name', 'issuing_organization')
    list_filter = ('date_obtained', 'expiration_date')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency', 'resume', 'order')
    search_fields = ('name',)
    list_filter = ('proficiency',)

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'position', 'email', 'phone', 'resume')
    search_fields = ('name', 'company', 'position', 'email', 'phone')
