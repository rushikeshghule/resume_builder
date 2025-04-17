from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.db import transaction

import os
import uuid
import json
import copy
from datetime import datetime

# Try to import WeasyPrint, but don't fail if it's not available
WEASYPRINT_AVAILABLE = False
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    # WeasyPrint not available, will use fallback for PDF generation
    pass

from .models import (
    Resume, Education, WorkExperience, 
    Skill, Project, Certification, 
    Language, Reference, ResumeTemplate, PersonalInfo
)
from .forms import (
    ResumeForm, PersonalInfoForm, EducationFormSet, WorkExperienceFormSet,
    SkillFormSet, ProjectFormSet, CertificationFormSet, LanguageFormSet,
    ReferenceFormSet
)

# Create your views here.
def home(request):
    """Home page view with introduction to the resume builder"""
    # Public view - show templates and marketing content
    templates = ResumeTemplate.objects.all()[:5]
    return render(request, 'resume/home.html', {'templates': templates})

def about(request):
    """About page with information about the application"""
    return render(request, 'resume/about.html')

@login_required
def dashboard(request):
    """Dashboard view showing user's resumes"""
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'resume/dashboard.html', {'resumes': resumes})

@login_required
def create_resume(request):
    """Create a new resume"""
    # Get templates outside the if/else to avoid UnboundLocalError
    templates = ResumeTemplate.objects.all()
    
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            # Create default empty personal info section
            PersonalInfo.objects.create(resume=resume)
            
            messages.success(request, 'Resume created successfully. Now add your details.')
            return redirect('edit_resume_section', slug=resume.slug, section='personal')
    else:
        form = ResumeForm()
    
    return render(request, 'resume/create_resume.html', {
        'form': form,
        'templates': templates
    })

def resume_preview(request, slug):
    """Preview the resume with the selected template"""
    resume = get_object_or_404(Resume, slug=slug)
    
    # Check permissions - either owner or public resume
    if not resume.is_public and (not request.user.is_authenticated or 
                                (resume.user != request.user and not request.user.is_staff)):
        raise PermissionDenied("You don't have permission to view this resume")
    
    # Get template ID from query parameters or use the resume's template
    template_id = request.GET.get('template_id')
    
    # Fetch all templates for the template switcher
    all_templates = ResumeTemplate.objects.all()
    
    # If template_id is provided, get the template object
    if template_id:
        try:
            current_template = ResumeTemplate.objects.get(id=template_id)
            # Create a temporary copy of the resume with the selected template
            preview_resume = copy.copy(resume)
            preview_resume.template = current_template
        except (ResumeTemplate.DoesNotExist, ValueError):
            # If template not found or invalid ID, use resume's original template
            preview_resume = resume
            current_template = resume.template
    else:
        # Use resume's original template
        preview_resume = resume
        current_template = resume.template
    
    context = {
        'resume': preview_resume,
        'original_resume': resume,
        'is_preview': True,
        'dark_mode': resume.is_dark_mode,
        'all_templates': all_templates,
        'current_template': current_template,
    }
    
    return render(request, 'resume/resume_preview.html', context)

@login_required
def edit_resume_section(request, slug, section):
    """Edit a specific section of the resume"""
    resume = get_object_or_404(Resume, slug=slug)
    
    # Check ownership
    if resume.user != request.user:
        raise PermissionDenied("You don't have permission to edit this resume")
    
    if section == 'personal':
        try:
            personal_info = resume.personal_info
        except PersonalInfo.DoesNotExist:
            personal_info = PersonalInfo.objects.create(resume=resume)
        
        if request.method == 'POST':
            form = PersonalInfoForm(request.POST, request.FILES, instance=personal_info)
            if form.is_valid():
                form.save()
                messages.success(request, 'Personal information updated successfully.')
                return redirect('edit_resume_section', slug=resume.slug, section='education')
        else:
            form = PersonalInfoForm(instance=personal_info)
        
        return render(request, 'resume/edit_personal.html', {
            'form': form,
            'resume': resume,
            'section': section
        })
    
    elif section == 'education':
        if request.method == 'POST':
            formset = EducationFormSet(request.POST, instance=resume)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Education information updated successfully.')
                return redirect('edit_resume_section', slug=resume.slug, section='experience')
        else:
            formset = EducationFormSet(instance=resume)
        
        return render(request, 'resume/edit_education.html', {
            'formset': formset,
            'resume': resume,
            'section': section
        })
    
    elif section == 'experience':
        if request.method == 'POST':
            formset = WorkExperienceFormSet(request.POST, instance=resume)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Work experience updated successfully.')
                return redirect('edit_resume_section', slug=resume.slug, section='skills')
        else:
            formset = WorkExperienceFormSet(instance=resume)
        
        return render(request, 'resume/edit_experience.html', {
            'formset': formset,
            'resume': resume,
            'section': section
        })
    
    elif section == 'skills':
        if request.method == 'POST':
            formset = SkillFormSet(request.POST, instance=resume)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Skills updated successfully.')
                return redirect('edit_resume_section', slug=resume.slug, section='projects')
        else:
            formset = SkillFormSet(instance=resume)
        
        return render(request, 'resume/edit_skills.html', {
            'formset': formset,
            'resume': resume,
            'section': section
        })
    
    elif section == 'projects':
        if request.method == 'POST':
            formset = ProjectFormSet(request.POST, instance=resume)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Projects updated successfully.')
                return redirect('edit_resume_section', slug=resume.slug, section='certifications')
        else:
            formset = ProjectFormSet(instance=resume)
        
        return render(request, 'resume/edit_projects.html', {
            'formset': formset,
            'resume': resume,
            'section': section
        })
    
    elif section == 'certifications':
        if request.method == 'POST':
            formset = CertificationFormSet(request.POST, instance=resume)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Certifications updated successfully.')
                return redirect('edit_resume_section', slug=resume.slug, section='languages')
        else:
            formset = CertificationFormSet(instance=resume)
        
        return render(request, 'resume/edit_certifications.html', {
            'formset': formset,
            'resume': resume,
            'section': section
        })
    
    elif section == 'languages':
        if request.method == 'POST':
            formset = LanguageFormSet(request.POST, instance=resume)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Languages updated successfully.')
                return redirect('edit_resume_section', slug=resume.slug, section='references')
        else:
            formset = LanguageFormSet(instance=resume)
        
        return render(request, 'resume/edit_languages.html', {
            'formset': formset,
            'resume': resume,
            'section': section
        })
    
    elif section == 'references':
        if request.method == 'POST':
            formset = ReferenceFormSet(request.POST, instance=resume)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'References updated successfully.')
                return redirect('resume_preview', slug=resume.slug)
        else:
            formset = ReferenceFormSet(instance=resume)
        
        return render(request, 'resume/edit_references.html', {
            'formset': formset,
            'resume': resume,
            'section': section
        })
    
    elif section == 'template':
        if request.method == 'POST':
            form = ResumeForm(request.POST, instance=resume)
            if form.is_valid():
                form.save()
                messages.success(request, 'Resume template updated successfully.')
                return redirect('resume_preview', slug=resume.slug)
        else:
            form = ResumeForm(instance=resume)
            templates = ResumeTemplate.objects.all()
        
        return render(request, 'resume/edit_template.html', {
            'form': form,
            'resume': resume,
            'templates': templates,
            'section': section
        })
    
    else:
        return redirect('dashboard')

@login_required
def delete_resume(request, slug):
    """Delete a resume"""
    resume = get_object_or_404(Resume, slug=slug)
    
    # Check ownership
    if resume.user != request.user:
        raise PermissionDenied("You don't have permission to delete this resume")
    
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Resume deleted successfully.')
        return redirect('dashboard')
    
    return render(request, 'resume/delete_resume.html', {'resume': resume})

def download_pdf(request, slug):
    """Generate and download a PDF version of the resume"""
    resume = get_object_or_404(Resume, slug=slug)
    
    # Check permissions
    if not resume.is_public and (not request.user.is_authenticated or 
                               (resume.user != request.user and not request.user.is_staff)):
        raise PermissionDenied("You don't have permission to download this resume")
    
    # Get template ID from query parameters
    template_id = request.GET.get('template_id')
    
    # If template_id is provided, get that template object
    if template_id:
        try:
            template = ResumeTemplate.objects.get(id=template_id)
            # Create a temporary copy of the resume with the selected template
            temp_resume = copy.copy(resume)
            temp_resume.template = template
            resume_for_pdf = temp_resume
        except (ResumeTemplate.DoesNotExist, ValueError):
            # If template not found or invalid ID, use resume's original template
            resume_for_pdf = resume
    else:
        # Use resume's original template
        resume_for_pdf = resume
    
    # Get template path
    template_path = f"resume/templates/{resume_for_pdf.template.template_file}"
    
    # Instead of modifying the model, prepare a context with extra data
    # Get the photo data as a base64 string if it exists
    photo_data_uri = None
    
    if (hasattr(resume_for_pdf, 'personal_info') and 
            hasattr(resume_for_pdf.personal_info, 'photo') and 
            resume_for_pdf.personal_info.photo):
        
        try:
            # Get the absolute path to the photo file
            photo_path = resume_for_pdf.personal_info.photo.path
            
            # Check if the file exists and create a data URI
            if os.path.exists(photo_path):
                import base64
                from PIL import Image
                import io
                
                # Open the image file
                with open(photo_path, 'rb') as img_file:
                    # Process the image
                    img = Image.open(img_file)
                    # Convert to RGB mode if it's RGBA to avoid transparency issues in PDF
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    
                    # Save to an in-memory bytes buffer
                    buffer = io.BytesIO()
                    img.save(buffer, format='JPEG')
                    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    # Create a data URI
                    photo_data_uri = f"data:image/jpeg;base64,{img_str}"
        except Exception as e:
            # Log the error but continue with PDF generation
            print(f"Error processing photo for PDF: {e}")
    
    # Prepare the context with the resume and additional data for the template
    context = {
        'resume': resume_for_pdf,
        'is_pdf': True,
        'photo_data_uri': photo_data_uri  # Pass the photo data URI to the template
    }
    
    # Render the template with resume data
    html_string = render_to_string(template_path, context)
    
    # Check if WeasyPrint is available
    if WEASYPRINT_AVAILABLE:
        try:
            # Use the base URL from the request to help resolve relative URLs
            base_url = f"{request.scheme}://{request.get_host()}"
            html = HTML(string=html_string, base_url=base_url)
            
            # Define CSS for better PDF rendering
            css = CSS(string='''
                @page {
                    size: letter;
                    margin: 0.5cm;
                }
                @media print {
                    body {
                        font-size: 12pt;
                        margin: 0;
                        padding: 0;
                    }
                    .resume-container {
                        margin: 0 !important;
                        box-shadow: none !important;
                    }
                }
            ''')
            
            # Generate PDF
            pdf = html.write_pdf(stylesheets=[css])
            
            # Create response
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"resume_{slugify(resume.title)}_{datetime.now().strftime('%Y%m%d')}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
        except Exception as e:
            # If WeasyPrint fails, fall back to HTML
            messages.error(request, f"PDF generation failed. Showing HTML preview instead. Error: {str(e)}")
            return render(request, template_path, context)
    else:
        # WeasyPrint not available, render HTML view instead
        messages.warning(request, "PDF generation is not available in this environment. Showing HTML preview instead.")
        return render(request, template_path, context)

def public_resume(request, slug):
    """View for public resume links"""
    resume = get_object_or_404(Resume, slug=slug, is_public=True)
    
    # Get template path
    template_name = resume.template.template_file if resume.template else 'modern.html'
    template_path = f"resume/templates/{template_name}"
    
    context = {
        'resume': resume,
        'is_public': True,
        'dark_mode': resume.is_dark_mode,
    }
    
    return render(request, template_path, context)

@login_required
def duplicate_resume(request, slug):
    """Create a duplicate of an existing resume"""
    original_resume = get_object_or_404(Resume, slug=slug)
    
    # Check ownership
    if original_resume.user != request.user:
        raise PermissionDenied("You don't have permission to duplicate this resume")
    
    with transaction.atomic():
        # Create new resume
        new_resume = Resume.objects.create(
            user=request.user,
            title=f"Copy of {original_resume.title}",
            template=original_resume.template,
            is_dark_mode=original_resume.is_dark_mode,
            is_public=False  # Default to private for the copy
        )
        
        # Copy personal info
        try:
            original_personal_info = original_resume.personal_info
            PersonalInfo.objects.create(
                resume=new_resume,
                first_name=original_personal_info.first_name,
                last_name=original_personal_info.last_name,
                job_title=original_personal_info.job_title,
                email=original_personal_info.email,
                phone=original_personal_info.phone,
                website=original_personal_info.website,
                linkedin=original_personal_info.linkedin,
                github=original_personal_info.github,
                twitter=original_personal_info.twitter,
                address=original_personal_info.address,
                city=original_personal_info.city,
                state=original_personal_info.state,
                zipcode=original_personal_info.zipcode,
                country=original_personal_info.country,
                summary=original_personal_info.summary,
            )
        except PersonalInfo.DoesNotExist:
            # Create a blank personal info if none exists
            PersonalInfo.objects.create(resume=new_resume)
        
        # Copy education entries
        for education in original_resume.education.all():
            Education.objects.create(
                resume=new_resume,
                institution=education.institution,
                degree=education.degree,
                field_of_study=education.field_of_study,
                location=education.location,
                start_date=education.start_date,
                end_date=education.end_date,
                is_current=education.is_current,
                description=education.description,
                gpa=education.gpa,
                order=education.order
            )
        
        # Copy work experience entries
        for experience in original_resume.work_experience.all():
            WorkExperience.objects.create(
                resume=new_resume,
                job_title=experience.job_title,
                company=experience.company,
                location=experience.location,
                start_date=experience.start_date,
                end_date=experience.end_date,
                is_current=experience.is_current,
                description=experience.description,
                achievements=experience.achievements,
                order=experience.order
            )
        
        # Copy skills
        for skill in original_resume.skills.all():
            Skill.objects.create(
                resume=new_resume,
                name=skill.name,
                level=skill.level,
                order=skill.order
            )
        
        # Copy projects
        for project in original_resume.projects.all():
            Project.objects.create(
                resume=new_resume,
                title=project.title,
                description=project.description,
                technologies=project.technologies,
                url=project.url,
                start_date=project.start_date,
                end_date=project.end_date,
                is_current=project.is_current,
                order=project.order
            )
        
        # Copy certifications
        for certification in original_resume.certifications.all():
            Certification.objects.create(
                resume=new_resume,
                name=certification.name,
                issuing_organization=certification.issuing_organization,
                date_obtained=certification.date_obtained,
                expiration_date=certification.expiration_date,
                credential_id=certification.credential_id,
                credential_url=certification.credential_url,
                description=certification.description,
                order=certification.order
            )
        
        # Copy languages
        for language in original_resume.languages.all():
            Language.objects.create(
                resume=new_resume,
                name=language.name,
                proficiency=language.proficiency,
                order=language.order
            )
        
        # Copy references
        for reference in original_resume.references.all():
            Reference.objects.create(
                resume=new_resume,
                name=reference.name,
                company=reference.company,
                position=reference.position,
                email=reference.email,
                phone=reference.phone,
                relationship=reference.relationship,
                reference_text=reference.reference_text,
                order=reference.order
            )
    
    messages.success(request, 'Resume duplicated successfully.')
    return redirect('dashboard')

@login_required
def toggle_resume_visibility(request, slug):
    """Toggle the public/private status of a resume"""
    if request.method == 'POST':
        resume = get_object_or_404(Resume, slug=slug)
        
        # Check ownership
        if resume.user != request.user:
            raise PermissionDenied("You don't have permission to modify this resume")
        
        resume.is_public = not resume.is_public
        resume.save()
        
        status = 'public' if resume.is_public else 'private'
        messages.success(request, f'Resume is now {status}.')
        
        return JsonResponse({'status': 'success', 'is_public': resume.is_public})
    
    return JsonResponse({'status': 'error'}, status=400)
