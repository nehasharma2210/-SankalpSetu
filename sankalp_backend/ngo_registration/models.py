from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class NGO(models.Model):
    CATEGORY_CHOICES = [
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
        ('environment', 'Environment'),
        ('poverty', 'Poverty Alleviation'),
        ('women_empowerment', 'Women Empowerment'),
        ('child_welfare', 'Child Welfare'),
        ('disaster_relief', 'Disaster Relief'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, help_text="Official name of the NGO")
    description = models.TextField(help_text="Brief description of NGO's mission and activities")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    website = models.URLField(blank=True, null=True, help_text="Official website URL")
    
    # Contact Information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    email = models.EmailField()
    
    # Address Information
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    
    # Legal Information
    registration_number = models.CharField(max_length=100, unique=True, help_text="Official registration number")
    registration_date = models.DateField(help_text="Date of official registration")
    tax_exempt_number = models.CharField(max_length=100, blank=True, null=True, help_text="Tax exemption number if applicable")
    
    # Additional Information
    founding_year = models.IntegerField(help_text="Year the NGO was founded")
    employee_count = models.IntegerField(help_text="Approximate number of employees")
    annual_budget = models.DecimalField(max_digits=12, decimal_places=2, help_text="Annual budget in INR")
    
    # Status and Timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name = "NGO"
        verbose_name_plural = "NGOs"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def full_address(self):
        address_parts = [self.address_line1]
        if self.address_line2:
            address_parts.append(self.address_line2)
        address_parts.extend([self.city, self.state, self.postal_code, self.country])
        return ', '.join(address_parts)


class NGODocument(models.Model):
    DOCUMENT_TYPES = [
        ('registration_certificate', 'Registration Certificate'),
        ('tax_exemption', 'Tax Exemption Certificate'),
        ('annual_report', 'Annual Report'),
        ('financial_statement', 'Financial Statement'),
        ('other', 'Other'),
    ]
    
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_name = models.CharField(max_length=255)
    document_file = models.FileField(upload_to='ngo_documents/', help_text="Upload relevant documents")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "NGO Document"
        verbose_name_plural = "NGO Documents"
    
    def __str__(self):
        return f"{self.ngo.name} - {self.document_type}"
