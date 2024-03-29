import random
import string
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import (update_session_auth_hash, login, views as
                                 auth_views)
from django.contrib.auth.decorators import (login_required, user_passes_test)
from django.contrib import messages
from django.db import transaction

from web.errors import (ICMSException, UnknownError)
from web.notify import address
from web.views import forms
from web.notify import notify
from web.auth.decorators import require_registered
from web import models
from .utils import form_utils
from .formset import (new_user_phones_formset, new_personal_emails_formset,
                      new_alternative_emails_formset)

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'web/login.html')


@require_registered
def home(request):
    return render(request, 'web/home.html')


def generate_temp_password(length=8):
    """
    Generates a random alphanumerical password of given length.
    Default length is 8
    """
    return ''.join(random.SystemRandom().choices(string.ascii_letters +
                                                 string.digits,
                                                 k=length))


def update_password(request):
    form = forms.PasswordChangeForm(
        request.user,
        request.POST or None,
        initial={'security_question': request.user.security_question})

    if form.is_valid():
        user = form.save(commit=False)
        user.register_complete = True
        user.save()
        update_session_auth_hash(request, user)  # keep user logged in

    return form


@user_passes_test(lambda u: u.is_anonymous, login_url='home')
def reset_password(request):
    action = request.POST.get('action') if request.POST else None
    login_id = request.POST.get('login_id', None)

    if action == 'reset_password':
        user = models.User.objects.get(username=login_id)
        form = forms.ResetPasswordSecondForm(user, request.POST or None)
        if form.is_valid():
            temp_pass = generate_temp_password()
            user.set_password(temp_pass)
            user.register_complete = False
            user.save()
            notify.register(request, user, temp_pass)
            return render(request,
                          'web/reset-password/reset-password-success.html')

        return render(request, 'web/reset-password/reset-password-2.html', {
            'form': form,
            'login_id': login_id
        })

    form = forms.ResetPasswordForm(request.POST or None)
    if form.is_valid():
        try:
            user = models.User.objects.get(
                username=form.cleaned_data.get('login_id', ''))
            form = forms.ResetPasswordSecondForm(user)
            return render(request, 'web/reset-password/reset-password-2.html',
                          {
                              'form': form,
                              'login_id': user.username
                          })
        except ObjectDoesNotExist:
            form.add_error(None, 'Invalid login id')

    return render(request, 'web/reset-password/reset-password-1.html',
                  {'form': form})


@login_required
def set_password(request):
    form = update_password(request)

    if form.is_valid():
        return redirect('home')

    return render(request, 'web/set-password.html', {'form': form})


@require_registered
def change_password(request):
    form = update_password(request)

    return render(request, 'web/user/password.html', {'form': form})


#  Redirect user to home if logged in already
@user_passes_test(lambda u: u.is_anonymous, login_url='home')
@transaction.atomic
def register(request):
    """
    An atomic transaction to save user information and send notifications
    When an unexpected error occurs the whole transaction is rolled back
    """
    # Handle security question
    data = request.POST.copy() if request.POST else None
    selected = request.POST.get('security_question_list', None)
    if selected and selected != forms.RegistrationForm.OWN_QUESTION:
        data['security_question'] = selected
    form = forms.RegistrationForm(data)
    captcha_form = forms.CaptchaForm(request.POST or None)
    if form.is_valid() and captcha_form.is_valid():
        user = form.instance
        temp_pass = generate_temp_password()
        user.set_password(temp_pass)
        user.username = user.email
        user.save()
        user.phone_numbers.create(phone=form.cleaned_data['telephone_number'])
        models.PersonalEmail(user=user,
                             email=user.email,
                             is_primary=True,
                             portal_notifications=True).save()
        notify.register(request, user, temp_pass)
        login(request, user)
        return redirect('set-password')

    return render(request, 'web/registration.html', {
        'form': form,
        'captcha_form': captcha_form
    })


@require_registered
def workbasket(request):
    process = models.AccessRequestProcess.objects.owned_process(request.user)
    return render(request, 'web/workbasket.html', {'process_list': process})


def init_user_details_forms(request, action):
    # If post is not made from user details page but from search page do not
    # try and initialise forms with POST data

    data = request.POST or None
    details_initial = None
    phones_initial = None
    alternative_emails_initial = None
    personal_emails_initial = None
    user = request.user

    if request.POST:
        if action == 'save_address':
            data = None
            user.work_address = request.POST.get('address')
            #: TODO: Save changes to session before search
            # Use new model to allow using initials
            # with edited values before searching for address
            # user = models.User()
            # user.id = request.user.id
            # user.work_address = request.POST.get('address')
            # details_initial = form_utils.remove_from_session(
            #     request, 'details_form')
            # phones_initial = form_utils.remove_from_session(
            #     request, 'phones_formset')
            # alternative_emails_initial = form_utils.remove_from_session(
            #     request, 'alternative_emails_formset')
            # personal_emails_initial = form_utils.remove_from_session(
            #     request, 'personal_emails_formset')

    details_form = forms.UserDetailsUpdateForm(data,
                                               initial=details_initial,
                                               instance=user)
    phones_formset = new_user_phones_formset(request,
                                             data=data,
                                             initial=phones_initial)
    alternative_emails_formset = new_alternative_emails_formset(
        request, data=data, initial=alternative_emails_initial)
    personal_emails_formset = new_personal_emails_formset(
        request, data=data, initial=personal_emails_initial)

    # get details form data from session if exists and not the first page load
    all_forms = {
        'details_form': details_form,
        'phones_formset': phones_formset,
        'alternative_emails_formset': alternative_emails_formset,
        'personal_emails_formset': personal_emails_formset
    }

    return all_forms


def address_search(request, action):
    if action == 'edit_address':  # Initial request
        postcode_form = forms.PostCodeSearchForm()
    else:
        postcode_form = forms.PostCodeSearchForm(request.POST)

    addresses = []
    if postcode_form.is_valid():
        try:
            addresses = address.find(
                postcode_form.cleaned_data.get('post_code'))
        except UnknownError:
            messages.warning(
                request, 'The postcode search system is currently unavailable,\
                please enter the address manually.')
        except ICMSException:
            postcode_form.add_error('post_code',
                                    'Please enter a valid postcode')

    return render(request, 'web/user/search-address.html', {
        'postcode_form': postcode_form,
        'addresses': addresses
    })


def manual_address(request, action):
    form = forms.ManualAddressEntryForm(request.POST or None)

    if form.is_valid():
        if action == 'save_manual_address':
            return details_update(request, 'save_address')

    return render(request, 'web/user/manual-address.html', {'form': form})


def details_update(request, action):
    forms = init_user_details_forms(request, action)
    if not action == 'save_address':
        if form_utils.forms_valid(forms):
            form_utils.save_forms(forms)
            # Create fresh forms  to remove objects before sending response
            forms['phones_formset'] = new_user_phones_formset(request)
            forms[
                'alternative_emails_formset'] = new_alternative_emails_formset(
                    request)
            forms['personal_emails_formset'] = new_personal_emails_formset(
                request)
            messages.success(request,
                             'Central contact details have been saved.')
        else:
            if request.POST:
                messages.error(request,
                               'Please correct the highlighted errors.')

    return render(request, 'web/user/details.html', forms)


@require_registered
def user_details(request):
    action = request.POST.get('action')
    if action in ['search_address', 'edit_address']:
        return address_search(request, action)
    elif action in ['manual_address', 'save_manual_address']:
        return manual_address(request, action)

    return details_update(request, action)


class LoginView(auth_views.LoginView):
    form_class = forms.LoginForm
    template_name = 'web/login.html'
    redirect_authenticated_user = True
