from .forms import ChangePasswordForm

def change_password_form(request):
    return {
        'form': ChangePasswordForm()
    }
