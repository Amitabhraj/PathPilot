from django.shortcuts import render,redirect
from django.contrib import messages
from PathPilot.decorators import login_required

@login_required
def upload_resume(request):
    if request.method == 'POST':
        resume = request.FILES.get('current_resume')

        if not resume:
            messages.error(request, "Please select a file.")
            return redirect('userHome')

        user = request.user
        user.current_resume = resume
        user.save()

        messages.success(request, "Resume uploaded successfully!")
        return redirect('userHome')

    return render(request, 'dashboard/user-home.html')