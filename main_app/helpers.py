from decimal import *
from .models import Category, LineItem

def update_category_price(li, new_cat, old_cat):
    # adds price to new cat, if old_cat is supplied then subtract from there

    # case: assigning li to new_cat
    new_cat.total += li.price

    # case: changing li from old cat to new cat
    if (old_cat != None):
        old_cat.total -= li.price

def update_category_titles(li, new_cat, old_cat):
    # adds titles to new cat, if old_cat is supplied then remove from there

    # case: assigning li to new_cat
    new_cat.titles += li.name

    # case: changing li from old cat to new cat
    if (old_cat != None):
        old_cat.titles = old_cat.titles.rsplit(";;",1)[0]