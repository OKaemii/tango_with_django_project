# must import project settings before django models to avoid error
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
# Django infrastructure has now been initialised.
import django
django.setup()
from rango.models import Category, Page

def populate():
    # creating a list of dics containing the pages we want to add into each category
    python_pages = [{"title": "Official Python Tutorial",
          "url":"http://docs.python.org/2/tutorial/"},
         {"title":"How to Think like a Computer Scientist",
          "url":"http://www.greenteapress.com/thinkpython/"},
         {"title":"Learn Python in 10 Minutes",
          "url":"http://www.korokithakis.net/tutorials/python/"}]

    django_pages = [
         {"title":"Official Django Tutorial",
          "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
         {"title":"Django Rocks",
          "url":"http://www.djangorocks.com/"},
         {"title":"How to Tango with Django",
          "url":"http://www.tangowithdjango.com/"} ]

    other_pages = [
         {"title":"Bottle",
          "url":"http://bottlepy.org/docs/dev/"},
         {"title":"Flask",
          "url":"http://flask.pocoo.org"} ]
    # creating a dictionary of dictionaries to allow iteration of each data structure
    cats = {"Python": {"pages": python_pages, "likes":64,"views":128},
             "Django": {"pages": django_pages, "likes":32,"views":64},
             "Other Frameworks": {"pages": other_pages, "likes":16,"views":32} }
    # if need add more categories/pages, add to dic above

    # goes through cats' dic, then add each category
    for cat, cat_data in cats.items():
        # c = add_cat(cat) # responsible for creation of categories
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"]) # responsible for creation of pages
    # print out categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    # use get_or_create() to create model instances in pop script, bc don't want dups of same entry
    # the get_or_create can check if entry exists in database, yes: createsself. returns a tuple(object - model instance, created - boolean)
    # thus, [0], since we only want d object.
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

# start execution here:
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
