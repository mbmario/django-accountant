from django.test import TestCase, Client
from testfixtures import compare
from .process_csv import *
from .analyze import *
from .models import *
from django.contrib.auth.models import User
from django.test import RequestFactory
from .forms import *
from .views import *

# tests from upload_csv
class TestCaseCSV(TestCase):


    def test_category_dict(self):
        default_user = User.objects.create(username="AzureDiamond", password="hunter2") # id will be 1 for defaults

        soap_titles = "SOAPSTORE;;CLEANING EMPORIUM;;SOAPSTORE;;BED BATH N BEYOND"
        candles_titles = "WAX CITY;;BED BATH N BEYOND;;SOAPSTORE"
        car_titles = ""
        soaps = Category.objects.create(name="soaps", titles=soap_titles)
        candles = Category.objects.create(name="candles", titles=candles_titles)
        cars = Category.objects.create(name="cars", titles=car_titles)
        rockets = Category.objects.create(name="rockets")

        desired_result = {"SOAPSTORE" : "soaps", "CLEANING EMPORIUM" : "soaps", "BED BATH N BEYOND": "candles", \
                           "WAX CITY" : "candles"}
        #pdb.set_trace()
        test_result = get_titles_dict()
        compare(desired_result, test_result)

    def test_process_line(self):

        # tests process_csv/process_line and its child fns
        # (method desc): takes  a line and formatting info (cols) and returns a "best guess" li item

        default_category = Category.objects.create(name="*uncategorized")
        gas = Category.objects.create(name="gas")
        restaurants = Category.objects.create(name="restaurants")
        lines = [
            "\"2/12/2018\",\"\",\"ARCO#82844               KENT         WA\",\"21.65\",\"\"",
            "\"Date\", \"No.\", \"Description\", \"Debit\", \"Credit\"",
            "\"2/19/2018\", \"\", \"Interest Charge on Cash Advances\", \"\", \"0.00\"",
            "\"2/11/2018\", \"\", \"LOVES TRAVEL S00004135   ELLENSBURG   WA\", \"9.19\", \"",
            "\"2/12/2018\", \"\", \"MCDONALD'S F13372        LIBERTY LAKE WA\", \"7.91\", \"\""
        ]
        desired_result = [
            LineItem(name="ARCO",
                     category=gas,
                     price='21.65',
                     date='2018-02-12',
                     info="ARCO#82844 KENT WA",
                     recent=True),
            None,
            None,
            LineItem(name="LOVES TRAVEL",
                     category=default_category,
                     price='9.19',
                     date='2018-02-11',
                     info="LOVES TRAVEL S00004135 ELLENSBURG WA",
                     recent=True,
                     user_id=1),
            LineItem(name="MCDONALD'S",
                     category=restaurants,
                     price='7.91',
                     date='2018-02-12',
                     info="MCDONALD'S F13372 LIBERTY LAKE WA",
                     recent=True),
        ]
        cols = {'price': 3, 'date': 0, 'info': 2}
        titles_dict= {"ARCO" : "gas", "MCDONALD'S" : "food"}

        compare(process_line(lines[0],cols, titles_dict, 1), desired_result[0])
        compare(process_line(lines[1], cols, titles_dict, 1), desired_result[1])
        compare(process_line(lines[2], cols, titles_dict, 1), desired_result[2])
        compare(process_line(lines[2], cols, titles_dict, 2), None) #wrong user

# tests post views
class TestCaseViews(TestCase):

    def test_assign_cat_to_li_good_data(self):
        #(method desc): changes the line item (li)'s category to the given category (cat)
        user1 = User.objects.create_user(username='alice', email='a@a.com',password='qwerty')
        user2 = User.objects.create_user(username='bob', email='b@b.com', password='qwerty')

        old_cat = Category.objects.create(name="*old_cat", total=2.00, user=user2)
        new_cat = Category.objects.create(name="*new_cat", total=2.00, user=user2)
        #pdb.set_trace()
        li = LineItem.objects.create(name="*test_li_1", category=old_cat, price=2.00, \
                                     date='2018-04-06', recent=True, user=user2)

        # change the category from old to new by sending a post request to assign_cat_to_li
        request_factory = RequestFactory()
        data = {'li': li.name, 'cat': new_cat.name, 'id': li.id}
        request = request_factory.post('/placeholder', data)

        assign_cat_to_li(request)

        # pull objects again
        li = LineItem.objects.get(id=li.id)
        old_cat = Category.objects.get(name=old_cat.name, user=user2)
        new_cat = Category.objects.get(name=new_cat.name, user=user2)

        # assert that the li's category is changed, and that the amount got transferred
        compare(li.category.name, new_cat.name)
        compare(li.recent, False)
        compare(old_cat.total, 0.00)
        compare(new_cat.total, 4.00)

        # assert that the new category has the title appended to it
        assert(li.name + ";;" in new_cat.titles)


    def test_assign_cat_to_li_bad_data(self):
        # now bad data (wrong cat and id), because we can't have the numbers screwed up somehow

        old_cat = Category.objects.create(name="*old_cat", total=0.00)
        new_cat = Category.objects.create(name="*new_cat", total=4.00)

        li = LineItem.objects.create(name="*test_li_1", category=old_cat, price=2.00, date='2018-04-06', recent=True)

        request_factory = RequestFactory()

        bad_data_1 = {'li': li.name, 'cat': old_cat.name, 'id': -1}
        bad_data_2 = {'li': li.name, 'cat': "*invalid", 'id': li.id}
        request_1 = request_factory.post('/placeholder', bad_data_1)
        request_2 = request_factory.post('/placeholder', bad_data_2)

        assign_cat_to_li(request_1)
        assign_cat_to_li(request_2)

        old_cat = Category.objects.get(name=old_cat.name)
        new_cat = Category.objects.get(name=new_cat.name)
        li = LineItem.objects.get(id=li.id)

        #ensure nothing changed
        compare(old_cat.total, 0.00)
        compare(new_cat.total, 4.00)
        compare(li.category.name, old_cat.name)

class TestCaseAnalyze(TestCase):

    def test_compare_month(self):
        compare(1,1)
        #pdb.set_trace()
        nov17 = '2017-11'
        mar18 = '2018-03'
        desired_result = ["November 2017", "December 2017","January 2018", \
                          "February 2018", "March 2018"]
        months = get_months(nov17, mar18)
        #pdb.set_trace()
        compare(months, desired_result)

    def test_analyze(self):
        beer = Category.objects.create(name="beer")
        soap = Category.objects.create(name="soap")

        # wrong user (default is 1)
        user1 = User.objects.create_user(username='alice', email='a@a.com',password='qwerty')
        user2 = User.objects.create_user(username='bob', email='b@b.com', password='qwerty')
        #pdb.set_trace()
        li = LineItem.objects.create(name="sout",
            category=beer, price=5.00, date='2018-01-06', user=user2)

        # out of scope
        li = LineItem.objects.create(name="pilsner", \
            category=beer, price=5.00, date='2015-01-06')

        # 1 soap in each Nov and Dec 17
        li = LineItem.objects.create(name="smooth citrus cleanse", \
            category=soap, price=1.00, date='2017-11-12')
        li = LineItem.objects.create(name="decorative soap", \
            category=soap, price=1.00, date='2017-12-12')

        # 2 beers in Jan 18
        li = LineItem.objects.create(name="pilsner", \
            category=beer, price=5.00, date='2018-01-06')
        li = LineItem.objects.create(name="icehouse", \
            category=beer, price=15.00, date='2018-01-01')

        # 1 soap in Jan 18
        li = LineItem.objects.create(name="lavender indulgence", \
            category=soap, price=12.00, date='2018-01-12')

        # 1 beer in Feb 18
        li = LineItem.objects.create(name="red beer", \
            category=beer, price=15.00, date='2018-02-01')

        # 2 soap in Feb 18
        li = LineItem.objects.create(name="ivory", \
            category=soap, price=4.00, date='2018-02-12')
        li = LineItem.objects.create(name="herbal explosion", \
            category=soap, price=9.99, date='2018-02-16')

        rows = analyze_month('2017-11', '2018-02', 1)

        desired_nov = [(False, "November 2017"), ("beer", 0.0), ("soap",1.00)]
        desired_dec = [(False, "December 2017"), ("beer", 0.0), ("soap",1.00)]
        desired_jan = [(False, "January 2018"), ("beer", 20.00), ("soap",12.00)]
        desired_feb = [(False, "February 2018"), ("beer", 15.00), ("soap",13.99)]
        desired_total = [(False, "Sum"), ("beer", 35.00), ("soap",27.99)]
        desired_rows = [desired_nov, desired_dec, desired_jan, desired_feb, desired_total]

        compare(rows,desired_rows)
