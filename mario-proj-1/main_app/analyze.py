from .models import LineItem, Category
import pdb

def get_months(start, end): # more fun to do manually than find a very specific package?

    # convert to int tuple
    start = start.split("-")
    start = [int(start[1]), int(start[0])]

    end = end.split("-")
    end = [int(end[1]), int(end[0])]

    months = ["January", "February", "March", "April", "May", "June", \
              "July", "August", "September", "October", "November", "December"]
    result_months = []

    pdb.set_trace()
    # buttons.js $('input.analyze') has assurance that start is before end
    while (True):

        # add to array
        add = months[start[0]-1] + " " + str(start[1])
        result_months.append(add)

        # break if caught up
        if (start[0] == end[0] and start[1] == end[1]): break

        # otherwise increment
        if (start[0] == 12):
            start[0] = 1
            start[1] += 1
        else:
            start[0] += 1

    return result_months

def month_code(month):
    months = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, \
              "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}
    return months[month.split(" ")[0]]


def sum_total(rows):
    # sums categories over time period captured in rows
    # takes in row deep list object, returns it with sum row
    #   loops over rows, adding sub totals to dict, then adds dict to last rows
    cat_names = Category.objects.all().values_list('name', flat=True)
    sum_row = [(False, "Sum")]
    cat_totals = dict(zip(cat_names, [0.00]*len(cat_names)))

    # ex row [(False, "January 2018"), ("beer", 20.00), ("soap",12.00)]
    for row in rows:
        for entry in row[1:]:
            cat_totals[entry[0]] += entry[1]

    for key in sorted(cat_totals.keys()):
        value = cat_totals[key]
        sum_row.append((key, round(value, 2)))

    rows = rows + [sum_row]
    return rows


def sum_month(row, month_num, year_num, user_id):
    # creates a list of (category, price) for totals for the given mo/yr

    categories = Category.objects.filter(user_id=user_id)
    month_lis = LineItem.objects.filter(date__month=month_num, date__year=year_num, user_id=user_id)

    for cat in categories:
        match_lis = month_lis.filter(category=cat)
        cat_sum = 0.0

        for match in match_lis:
            cat_sum += float(match.price)

        row.append((cat.name, round(cat_sum,2)))

    return row

def analyze_month(start, end, user_id):
    # takes a start and end month in the format YYYY-MM
    # returns a deep list of rows for the results table
    # rows (main list of month rows)
    # month row (list of the month then (category,price) tuples)

    months = get_months(start, end) # just a type converter

    rows = []

    for month in months:

        row = []

        month_num = month_code(month)
        year_num = month.split(" ")[1]

        row.append((False, month))

        row = sum_month(row, month_num, year_num, user_id) # does the query work

        rows.append(row)

    rows = sum_total(rows) # sum over the rows, add as a final row

    return rows

