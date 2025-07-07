from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import NGO, NGODocument
import json
from datetime import datetime

def registration_form(request):
    """Display the NGO registration form"""
    context = {
        'title': 'NGO Registration',
        'categories': NGO.CATEGORY_CHOICES,
    }
    return render(request, 'ngo_registration/registration_form.html', context)

@csrf_exempt
def register_ngo(request):
    """Handle NGO registration form submission"""
    if request.method == 'POST':
        try:
            # Get form data
            data = request.POST
            
            # Validate required fields
            required_fields = [
                'name', 'description', 'phone_number', 'email',
                'address_line1', 'city', 'state', 'postal_code',
                'registration_number', 'registration_date', 'founding_year',
                'employee_count', 'annual_budget'
            ]
            
            for field in required_fields:
                if not data.get(field):
                    messages.error(request, f'Field {field.replace("_", " ").title()} is required.')
                    return redirect('ngo_registration:registration_form')
            
            # Check if registration number already exists
            if NGO.objects.filter(registration_number=data.get('registration_number')).exists():
                messages.error(request, 'An NGO with this registration number already exists.')
                return redirect('ngo_registration:registration_form')
            
            # Parse registration date
            try:
                registration_date = datetime.strptime(data.get('registration_date'), '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid registration date format. Please use YYYY-MM-DD.')
                return redirect('ngo_registration:registration_form')
            
            # Create NGO with transaction
            with transaction.atomic():
                ngo = NGO.objects.create(
                    name=data.get('name'),
                    description=data.get('description'),
                    category=data.get('category', 'other'),
                    website=data.get('website', ''),
                    phone_number=data.get('phone_number'),
                    email=data.get('email'),
                    address_line1=data.get('address_line1'),
                    address_line2=data.get('address_line2', ''),
                    city=data.get('city'),
                    state=data.get('state'),
                    postal_code=data.get('postal_code'),
                    country=data.get('country', 'India'),
                    registration_number=data.get('registration_number'),
                    registration_date=registration_date,
                    tax_exempt_number=data.get('tax_exempt_number', ''),
                    founding_year=int(data.get('founding_year')),
                    employee_count=int(data.get('employee_count')),
                    annual_budget=float(data.get('annual_budget')),
                    created_by=request.user if request.user.is_authenticated else None
                )
                
                # Handle file uploads
                if request.FILES:
                    for file_key, file_obj in request.FILES.items():
                        if file_key.startswith('document_'):
                            document_type = data.get(f'doc_type_{file_key.split("_")[1]}', 'other')
                            NGODocument.objects.create(
                                ngo=ngo,
                                document_type=document_type,
                                document_name=file_obj.name,
                                document_file=file_obj
                            )
            
            messages.success(request, f'NGO "{ngo.name}" has been registered successfully! Registration ID: {ngo.id}')
            return redirect('ngo_registration:registration_success')
            
        except ValueError as e:
            messages.error(request, f'Invalid data format: {str(e)}')
            return redirect('ngo_registration:registration_form')
        except Exception as e:
            messages.error(request, f'An error occurred during registration: {str(e)}')
            return redirect('ngo_registration:registration_form')
    
    return redirect('ngo_registration:registration_form')

def registration_success(request):
    """Display registration success page"""
    return render(request, 'ngo_registration/registration_success.html', {
        'title': 'Registration Successful'
    })

def ngo_list(request):
    """Display list of registered NGOs"""
    # Get filter parameters
    category_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    # Start with all NGOs
    ngos = NGO.objects.all()
    
    # Apply filters
    if category_filter:
        ngos = ngos.filter(category=category_filter)
    
    if status_filter:
        ngos = ngos.filter(status=status_filter)
    
    if search_query:
        ngos = ngos.filter(
            name__icontains=search_query
        ).distinct()
    
    # Pagination
    paginator = Paginator(ngos, 10)  # Show 10 NGOs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Registered NGOs',
        'page_obj': page_obj,
        'categories': NGO.CATEGORY_CHOICES,
        'statuses': NGO.STATUS_CHOICES,
        'current_filters': {
            'category': category_filter,
            'status': status_filter,
            'search': search_query,
        }
    }
    
    return render(request, 'ngo_registration/ngo_list.html', context)

def ngo_detail(request, ngo_id):
    """Display detailed information about a specific NGO"""
    ngo = get_object_or_404(NGO, id=ngo_id)
    documents = ngo.documents.all()
    
    context = {
        'title': f'NGO Details - {ngo.name}',
        'ngo': ngo,
        'documents': documents,
    }
    
    return render(request, 'ngo_registration/ngo_detail.html', context)

@login_required
def update_ngo_status(request, ngo_id):
    """Update NGO status (admin functionality)"""
    if request.method == 'POST' and request.user.is_staff:
        ngo = get_object_or_404(NGO, id=ngo_id)
        new_status = request.POST.get('status')
        
        if new_status in [choice[0] for choice in NGO.STATUS_CHOICES]:
            ngo.status = new_status
            ngo.save()
            messages.success(request, f'NGO status updated to {new_status}.')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('ngo_registration:ngo_list')

def api_ngo_stats(request):
    """API endpoint for NGO statistics"""
    stats = {
        'total_ngos': NGO.objects.count(),
        'pending_registrations': NGO.objects.filter(status='pending').count(),
        'approved_ngos': NGO.objects.filter(status='approved').count(),
        'rejected_applications': NGO.objects.filter(status='rejected').count(),
        'categories': {}
    }
    
    # Get category-wise count
    for category_code, category_name in NGO.CATEGORY_CHOICES:
        stats['categories'][category_name] = NGO.objects.filter(category=category_code).count()
    
    return JsonResponse(stats)
