from django.shortcuts import render
from django.http import HttpResponse

def idea_list(request):
    """Display list of ideas"""
    return render(request, 'ideas/idea_list.html', {
        'title': 'Ideas List',
        'message': 'Ideas functionality is coming soon!'
    })

def submit_idea(request):
    """Display idea submission form"""
    return render(request, 'ideas/submit_idea.html', {
        'title': 'Submit Idea',
        'message': 'Idea submission functionality is coming soon!'
    })

def idea_detail(request, idea_id):
    """Display idea details"""
    return render(request, 'ideas/idea_detail.html', {
        'title': f'Idea #{idea_id}',
        'idea_id': idea_id,
        'message': 'Idea details functionality is coming soon!'
    })
