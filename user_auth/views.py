from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib import messages
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect
from .forms import SignUpForm
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives


#define signup view
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'There were some problems while creating account')
            context = RequestContext(request,{'form' : form})
            return render_to_response('auth/signup.html', context)
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password, email=email)
            #print user.is_active
            user.is_active = False
            #print user.is_active
            user.save()
            send_email_activation(user, request)
            messages.add_message(request, messages.SUCCESS, 'Your account is created, activate it through the link in your email')
            return HttpResponseRedirect('/signin')
    else:
        context = RequestContext(request, {'form':SignUpForm()})
        return render_to_response('auth/signup.html', context)

def signin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if 'next' in request.GET:
                        return HttpResponseRedirect(request.get['next'])
                    else:
                        return HttpResponseRedirect('/')
                else:
                    messages.add_message(request, messages.ERROR, 'Your account is deactivated')
                    context = RequestContext(request)
                    return render_to_response('auth/signin.html', context)
            else:
                messages.add_message(request, messages.ERROR, 'Username or Password Invalid')
                context = RequestContext(request)
                return render_to_response('auth/signin.html', context)
        else:
            context = RequestContext(request)
            return render_to_response('auth/signin.html', context)


def signout(request):
    logout(request)
    return HttpResponseRedirect('/signup')

def reset(request):
    return password_reset(request,
                          template_name='auth/reset.html',
                          email_template_name='auth/reset_email.html',
                          subject_template_name='auth/reset_subject.txt',
                          post_reset_redirect='/success')

def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request,
                                  template_name='auth/reset_confirm.html',
                                  uidb64=uidb64,
                                  token=token,
                                  post_reset_redirect=reverse('signin'))

def success(request):
    return render(request, 'auth/success.html')

# To activate the account of the user through the email
def send_email_activation(user,request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    from_email = 'sivaponugoti@gmail.com'
    to_email = user.email
    context = RequestContext(request)
    email_content = {'email':to_email, 'token':token, 'uid':uid}
    context.update(email_content)
    subject = loader.render_to_string('auth/account_activate.txt', context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string('auth/account_activate.html', context)
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    '''
    if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')
    '''
    email_message.send()

def activate_account(request, uidb64=None, token=None):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if user and default_token_generator.check_token(user,token):
        if user.is_active:
            messages.add_message(request, messages.SUCCESS, 'Your account is already activated a while ago')
        else:
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your account is activated')
    return HttpResponseRedirect('/signin')




