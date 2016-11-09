from django.contrib.auth.models import User

from callboard.models import Category,SubCategory,Goods
from django.db import transaction

TEXT = 'Объявление № '
BODY = 'Описание № '
CONDITION = 'New'

#
# 12
# 45




@transaction.atomic
def main(count,cat_id,sub_id, username):
    CATEGORY = Category.objects.get(pk=cat_id)
    SUBCATEGORY = SubCategory.objects.get(pk=sub_id)
    USER = User.objects.get(username=username)
    for i in range(count):
        good = Goods(category=CATEGORY,subcategory=SUBCATEGORY,name=TEXT+str(i+1),description=BODY+str(i+1),condition=CONDITION, price=i+1+100, user=USER)
        good.save()


if __name__ == '__main__':
      main()

