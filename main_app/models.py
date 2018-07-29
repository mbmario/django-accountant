from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# note on Category's "titles":
#  the Category will store multiple identical titles to count as "votes" for a particular category
#   so that when a li's category is changed, the entire db will not have to be iterated through or kept track of
#   under the assumption that conflicts are rare and category asssignments are common
#   titles correspond to li.names, but should not be seen as foreign keys
class Category(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=100, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    titles = models.TextField(default="", null=True) # e.g. "SOAPSTORE;;CLEANING EMPORIUM;;SOAPSTORE;;BED BATH N BEYOND"

    class Meta:
        unique_together = ("user", "name")

        # def __str__(self):
    #     return "\nname: " + self.name + "\n" + \
    #             "id: " + str(self.id) + "\n" + \
    #             "user id: " + str(self.user_id) + "\n" + \
    #             "total: " + str(self.total) + "\n" + "\n"



class LineItem(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateField(default='1990-01-01')
    recent = models.BooleanField(default=False)
    info = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name + "\n\t" + \
                "id: " + str(self.id) + "\n\t" + \
                "user_id: " + str(self.user_id) + "\n\t" + \
                "category: " + self.category.name + "\n\t" + \
                "category id: " + str(self.category.id) + "\n\t" + \
                "price: " + str(self.price) + "\n\t" + \
                "date: " + str(self.date) + "\n\t" + \
                "recent: " + str(self.recent) + "\n\t" + \
                "info: " + self.info + "\n"