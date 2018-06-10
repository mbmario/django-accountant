# the process to turn csvs into new lis
from decimal import *
import pdb

def get_cols():
    # returns column info based on banks' formatting

    bank = "BECU" # few enough banks that we can hard-code csv cols

    if (bank == "BECU"):
        return {'price': 3, 'date': 0, 'info': 2}

    return {'price': 3, 'date': 0, 'info': 2} # default to BECU's format

def format_date(unformatted):
    # format date utility method

    # needs to be YYYY-MM-DD
    # BECU is '2/19/2018'
    from dateutil import parser
    date = parser.parse(unformatted)
    return date.strftime('%Y-%m-%d')

def clean_info(raw_info):
    return raw_info.replace("  ","").replace("\t", "").replace("\"","")

def clean_name(info):
    # returns the name, getting it from removing pound symbols, numbers, whitespace from info
    import re
    name = info.split("  ")[0]
    name = name.split("#")[0]
    name = re.compile("([0-9])\w+").split(name)[0]
    return name

def guess_cat(title, titles_dict):
    # guesses correct category based on keywords
    # {title: most common category with alphabetical tie break}
    if title in titles_dict.keys():
        return titles_dict[title]
    return "*uncategorized"

def process_line(line, cols, titles_dict, user_id):
    # takes  a line and formatting info (cols) and returns a "best guess" li item
    # updates and returns dictionary of titles
    from .models import LineItem, Category
    import re

    # parse list into a line
    line_list = line.rstrip('\n').split(",")
    line_list = [str.replace("\"", "") for str in line_list]

    # skip empty or nonlines
    price = line_list[cols['price']]
    if re.search('[a-zA-Z]', price) is not None or price.strip() is "":
        return

    # process fields using helper methods
    date = format_date(line_list[cols['date']])
    info = clean_info(line_list[cols['info']])
    name = clean_name(info)
    cat_name = guess_cat(name, titles_dict)
    cat = Category.objects.get(name=cat_name, user_id=user_id)

    li = LineItem(name=name,
                  category=cat,
                  price=price,
                  date=date,
                  info=clean_info(info),
                  user_id=user_id,
                  recent=True)
    return li

def update_category_price(li,user_id):
    # updates the totals of the default category
    from .models import Category

    cat_name = li.category
    price = li.price
    import pdb
    #pdb.set_trace()

    # if the category exists, update
    if Category.objects.filter(name=cat_name, user_id=user_id).count() is not 0:
        cat = Category.objects.get(name=cat_name, user_id=user_id)
        cat.total = cat.total + Decimal(price)

    # if the category doesn't exist, create it
    else:
        cat = Category(name=cat_name, total=price, user_id=user_id)

    cat.save()

def get_titles_dict():
    # returns a dictionary of li name ("title") : category
    # this will be static during the upload, so just a single call to db for titles field

    # NOTE:
    # the db will store multiple identical titles to count as "votes" for a particular category
    #   so that when a li's category is changed, the entire db will not have to be iterated through or kept track of
    #   under the assumption that conflicts are rare and category asssignments are common

    # here, we assign the li name (title) to all category votes that appear
    # then in a second step, condense this for a more usable dictionary
    # this is more complicated than I thought it would be but it was fun
    from .models import Category

    weights = {} # {title, [category1, category1, category2, etc],
    titles_dict = {} # {title: most common category with alphabetical tie break}

    cats = Category.objects.all()

    # make the initial weights dict
    for cat in cats:

        #if there are no titles then our work is done, the lis will be *unassigned
        if cat.titles is None:
            break
        elif cat.titles is "":
            break

        cat_name = cat.name
        titles = cat.titles.split(";;")


        for title in titles:
            # if the title is not in the dictionary, add title : [category]
            # if it is already in the dictionary, append category to the title spot
            if title not in weights:
                weights[title] = [cat_name]
            else:
                weights[title].append(cat_name)

    # now condense to titles_dict by letting the votes vote
    for title in weights.keys():
        all = weights[title]
        uniques = list(set(all)) # unique categories in this set
        winner = uniques[0]
        winner_ct = 0

        for unique in uniques:
            unique_ct = all.count(unique)
            if  unique_ct > winner_ct: # a new most common; update
                winner = unique
                winner_ct = unique_ct
            if unique_ct == winner_ct: # tie goes to first alphabetically
                winner = min(winner, unique)

        titles_dict[title] = winner

    return titles_dict




def process_csv(f, user_id):
    # wrapper fn; takes a file and iterates through lines
    # calls process_line to turn line into li, then saves and updates category total

    from io import TextIOWrapper

    text_f = TextIOWrapper(f.file, encoding='utf-8')

    cols = get_cols()

    for line in text_f.readlines():

        li = process_line(line, cols, get_titles_dict(), user_id)
        if li is not None:
            li.save()
            update_category_price(li, user_id)

