from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import (
    Resume, PersonalInfo, Education, WorkExperience, 
    Skill, Project, Certification, Language, Reference,
    ResumeTemplate
)
from django.utils.text import slugify

class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'template', 'is_dark_mode', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resume Title'}),
        }

class PersonalInfoForm(ModelForm):
    class Meta:
        model = PersonalInfo
        exclude = ['resume']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn URL'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub URL'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Twitter URL'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State/Province'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip/Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Professional Summary', 'rows': 4}),
        }

class EducationForm(ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = Education
        exclude = ['resume', 'order']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institution'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Degree'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Field of Study'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 3}),
            'gpa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GPA'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class WorkExperienceForm(ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = WorkExperience
        exclude = ['resume', 'order']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Description', 'rows': 3}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Key Achievements', 'rows': 3}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        exclude = ['resume', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skill Name'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
        }

class ProjectForm(ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = Project
        exclude = ['resume', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Project Description', 'rows': 3}),
            'technologies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Technologies Used'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Project URL'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CertificationForm(ModelForm):
    date_obtained = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )
    expiration_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = Certification
        exclude = ['resume', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Certification Name'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Issuing Organization'}),
            'credential_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Credential ID'}),
            'credential_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Credential URL'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 3}),
        }

class LanguageForm(ModelForm):
    class Meta:
        model = Language
        exclude = ['resume', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Language'}),
            'proficiency': forms.Select(attrs={'class': 'form-select'}),
        }

class ReferenceForm(ModelForm):
    class Meta:
        model = Reference
        exclude = ['resume', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference Name'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship'}),
            'reference_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Reference Text', 'rows': 3}),
        }

# Create formsets for sections that can have multiple items
EducationFormSet = inlineformset_factory(
    Resume, Education, form=EducationForm, 
    extra=1, can_delete=True, can_delete_extra=True
)

WorkExperienceFormSet = inlineformset_factory(
    Resume, WorkExperience, form=WorkExperienceForm, 
    extra=1, can_delete=True, can_delete_extra=True
)

SkillFormSet = inlineformset_factory(
    Resume, Skill, form=SkillForm, 
    extra=3, can_delete=True, can_delete_extra=True
)

ProjectFormSet = inlineformset_factory(
    Resume, Project, form=ProjectForm, 
    extra=1, can_delete=True, can_delete_extra=True
)

CertificationFormSet = inlineformset_factory(
    Resume, Certification, form=CertificationForm, 
    extra=1, can_delete=True, can_delete_extra=True
)

LanguageFormSet = inlineformset_factory(
    Resume, Language, form=LanguageForm, 
    extra=1, can_delete=True, can_delete_extra=True
)

ReferenceFormSet = inlineformset_factory(
    Resume, Reference, form=ReferenceForm, 
    extra=1, can_delete=True, can_delete_extra=True
)
