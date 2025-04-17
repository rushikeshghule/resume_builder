from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class ResumeTemplate(models.Model):
    """Model to store resume template information"""
    name = models.CharField(max_length=100)
    preview_image = models.ImageField(upload_to='template_previews/', null=True, blank=True)
    template_file = models.CharField(max_length=100)  # Template file name (e.g., 'modern.html')
    is_dark_mode_supported = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Resume(models.Model):
    """Main resume model that links to a user and contains all resume sections"""
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes', null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True)
    is_dark_mode = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    guest_email = models.EmailField(blank=True, null=True)  # For non-registered users
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            # Ensure the slug is unique
            while Resume.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('resume_detail', args=[self.slug])
    
    def __str__(self):
        return self.title

class PersonalInfo(models.Model):
    """Model to store personal information"""
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='personal_info')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Education(models.Model):
    """Model to store education information"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    gpa = models.CharField(max_length=10, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-end_date', '-start_date']
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"

class WorkExperience(models.Model):
    """Model to store work experience information"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='work_experience')
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-end_date', '-start_date']
    
    def __str__(self):
        return f"{self.job_title} at {self.company}"

class Skill(models.Model):
    """Model to store skills information"""
    SKILL_LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    )
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Project(models.Model):
    """Model to store projects information"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    technologies = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-end_date', '-start_date']
    
    def __str__(self):
        return self.title

class Certification(models.Model):
    """Model to store certifications information"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    date_obtained = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-date_obtained']
    
    def __str__(self):
        return self.name

class Language(models.Model):
    """Model to store language proficiency information"""
    PROFICIENCY_CHOICES = (
        ('elementary', 'Elementary'),
        ('limited_working', 'Limited Working'),
        ('professional_working', 'Professional Working'),
        ('full_professional', 'Full Professional'),
        ('native', 'Native/Bilingual'),
    )
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Reference(models.Model):
    """Model to store reference information"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='references')
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    relationship = models.CharField(max_length=100, blank=True)
    reference_text = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
