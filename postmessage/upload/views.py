from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UploadForm , UserRegistrationForm
from .models import Upload
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login ,logout


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def upload_list(request):
    uploads = Upload.objects.all().order_by('-created_at') 
    return render(request, 'upload_list.html', {'uploads': uploads})

@login_required
def upload_create(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            return redirect('upload_list')
    else:
        form = UploadForm()  
    return render(request, 'upload_form.html', {'form': form})

@login_required
def upload_edit(request, upload_id):
    upload = get_object_or_404(Upload, pk=upload_id, user=request.user) 
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES, instance=upload)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            return redirect('upload_list')
    else:
        form = UploadForm(instance=upload) 
    return render(request, 'upload_form.html', {'form': form})

@login_required
def upload_delete(request, upload_id):
    upload = get_object_or_404(Upload, pk=upload_id, user=request.user)  
    if request.method == 'POST':
        upload.delete()
        return redirect('upload_list') 
    return render(request, 'upload_confirm_delete.html', {'upload': upload})  

def register(request):
    if request.method=='POST':
      form = UserRegistrationForm(request.POST)
      if form.is_valid():
          user = form.save(commit=False)
          user.set_password(form.cleaned_data['password1'])
          user.save()
          login(request, user)
          return redirect('upload_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html',{'form': form})

@login_required
def user_logout(request):
    # Check if the request is a POST
    if request.method == 'POST':
        # Perform logout
        logout(request)
        # Redirect to a 'logout successful' page
        return redirect('upload_list')
    else:
        # If it's a GET request, render a confirmation page or just show the logout page
        return render(request, 'logout.html') 
    
def upload_search(request):
    query = request.GET.get('q', '')
    print(f"Search query: {query}")  # Debugging line
    uploads = Upload.objects.filter(text__icontains=query) | Upload.objects.filter(user__username__icontains=query)
    print(f"Found uploads: {uploads}")  # Debugging line
    return render(request, 'search.html', {'uploads': uploads})

