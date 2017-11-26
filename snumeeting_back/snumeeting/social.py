from django.shortcuts import redirect
from django.contrib import messages

def check_user(strategy, user, request, **kwargs):
  print(user)
  print(kwargs)

  if user is None and kwargs.get('is_new'):
    messages.error(request, 'To use this, you need to connect your account first.')
    return redirect('http://localhost:4200/sign_in')