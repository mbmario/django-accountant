from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse


from .models import Category, LineItem, User
from .forms import CatForm, LIForm, UploadFileForm
from .helpers import *
from .process_csv import process_csv
from django.shortcuts import redirect
from .analyze import analyze_month
import pdb

### Pages ###
def index(request):

    categories = Category.objects.all()
    lineItems_new = LineItem.objects.filter(recent=True)
    lineItems_old = LineItem.objects.filter(recent=False)

    return render(request, 'index.html', {'categories': categories, 'lineItems_new': lineItems_new, 'lineItems_old': lineItems_old})


def upload_manual(request):
    categories = Category.objects.all()
    lineItems = LineItem.objects.all()

    catForm = CatForm()
    liForm = LIForm()

    context = {'categories': categories, 'lineItems': lineItems, 'catForm': catForm, 'liForm': liForm}
    return render(request, 'upload_manual.html', context)


def add_cat(request):

    categories = Category.objects.all()
    lineItems = LineItem.objects.all()

    catForm = CatForm()

    context = {'categories': categories, 'lineItems': lineItems, 'catForm': catForm}
    return render(request, 'add_cat.html', context)


def add_li(request):
    categories = Category.objects.all()
    lineItems = LineItem.objects.all()

    liForm = LIForm()

    context = {'categories': categories, 'lineItems': lineItems, 'liForm': liForm}
    return render(request, 'add_li.html', context)

def post_cat(request):
    # processes a new category

    form = CatForm(request.POST)
    if form.is_valid():
        user_id = request.user.id
        pdb.set_trace()
        if user_id == None:  user_id = User.objects.get(username='default').id
        cat = Category(name=form.cleaned_data['name'],
                       total=form.cleaned_data['total'],
                       user_id=user_id)
        cat.save()
    return HttpResponseRedirect('/')


def post_li(request):
    # processes a new line item

    form = LIForm(request.POST)
    if form.is_valid():
        user_id = request.user.id
        if user_id == None:  user_id = User.objects.get(username='default').id
        category_name = form.cleaned_data['category']
        price = price=form.cleaned_data['price']

        # update the Category collection: add if not there, add total if there
        matches = Category.objects.filter(name=category_name, user_id=user_id)



        if(not matches): # add the cat entry (may be blocked by dropdown, but available in future)
            cat = Category(name=category_name, total=price, user_id=user_id)
            cat.save()

            li = LineItem(name=form.cleaned_data['name'],
            category=cat,
            price=price,
            date=form.cleaned_data['date'],
            info=form.cleaned_data['info'],
            user_id=user_id,
            recent=False)
            li.save()

        else: # update the cat's total & titles
            cat = Category.objects.filter(name=category_name, user_id=user_id).first()

            # add the LI
            li = LineItem(name=form.cleaned_data['name'],
                category=cat,
                price=price,
                date=form.cleaned_data['date'],
                info=form.cleaned_data['info'],
                user_id=user_id,
                recent=False)
            li.save()
            update_category_price(li, cat, None)
            update_category_titles(li, cat, None)

    return HttpResponseRedirect('/')

def assign_cat_to_li(request):
    # changes the line item (li)'s category to the given category (cat)
    # works with an AJAX request from modify_li.js

    li_id = request.POST.get('id', None)
    new_cat_name = request.POST.get('cat', None) # string

    # query to get objects
    try:
        li = LineItem.objects.get(id=li_id)
        old_cat = name=li.category
        new_cat = Category.objects.get(name=new_cat_name, user=li.user)

    except:
        return # can't trust jquery

    # update li object with the new cateogy, and ensure it is touched
    li.category = new_cat
    li.recent = False
    li.save()

    update_category_price(li, new_cat, old_cat)
    update_category_titles(li, new_cat, old_cat)

    return HttpResponse(new_cat.name)


def upload_csv(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            user_id = request.user.id
            if user_id == None:  user_id = User.objects.get(username='default').id
            process_csv(request.FILES['file'], user_id)
            return HttpResponseRedirect('/')


    form = UploadFileForm()
    return render(request, 'upload_csv.html', {'form' : form})


def button_input(request):
    # receives misc button changes

    user_id = request.user.id
    if user_id == None:  user_id = User.objects.get(username='default').id
    action = request.POST.get('action')
    id = request.POST.get('id')
    value = request.POST.get('value')
    #pdb.set_trace()

    # "all ok" mark all as recent
    if action == "all ok":
        new_lis = LineItem.objects.filter(recent=True, user_id=user_id)
        #pdb.set_trace()
        for li in new_lis:
            li.recent = False
            li.save()
        return HttpResponseRedirect('/')

    #delete button
    if "delete" in action:
        if "li" in action:
            LineItem.objects.filter(id=id).delete()
        else:
            Category.objects.filter(id=id).delete()
        return id

# analyze button
def analyze(request, range):

    start = range.split(":")[0]
    end = range.split(":")[1]
    user_id = request.user.id
    if user_id == None:  user_id = User.objects.get(username='default').id
    rows = analyze_month(start, end, user_id)
    return render(request, 'analyze.html', {'rows': rows})
