# Create your views here.
from userforms.forms import FunkyForm
from django.shortcuts import render, redirect
from django.contrib import messages
from userforms.models import UserForm


def index(request):

    curr_page = request.current_page.id if request.current_page.publisher_is_draft else request.current_page.publisher_draft.id

    try:
        user_form = UserForm.objects.get(cms_pages=curr_page)
    except UserForm.DoesNotExist:
        return render(request, 'userforms/index.html', {'noform': True})
    except UserForm.MultipleObjectsReturned:
        return render(request, 'userforms/index.html', {'multipleform': True})

    form = FunkyForm(user_form=user_form)

    # If POST then validate and save data to database
    if request.method == 'POST' and request.POST.get('user_form_id'):

        form.data = request.POST.copy()
        form.files = request.FILES.copy()
        form.is_bound = True

        if form.is_valid():
            # Saving to database
            form.save(user_form=user_form)
            # Display success message
            messages.add_message(request, messages.SUCCESS, user_form.text_after_send)
            return redirect('userforms_success')
        else:
            return render(request, 'userforms/index.html', {'form_meta': user_form, 'form': form})
    else:
        # ELSE showing form
        return render(request, 'userforms/index.html', {'form_meta': user_form, 'form': form})


def success(request):
    return render(request, 'userforms/success.html')