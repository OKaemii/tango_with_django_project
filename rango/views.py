from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import render
from django.http import HttpResponse
# importing catergory model
from rango.models import Category
from rango.models import Page


def index(request):
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary
	# that will be passed to the template engine.
	# the "-" in "likes" tells it that we want it in descending order, and [:5] will return the first five.
	category_list = Category.objects.order_by('-likes')[:5]

	page_list = Page.objects.order_by('-views')[:5]

	context_dict = {'categories': category_list, 'pages': page_list}
	# contruct a dic to pass to the template engine as its contxtself.
	# note the key boldmessage shld be same as {{ x }} from the templateself.
	#context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	# return a rendered reponse to send to the clientself.
	# using shortcuts function to make life easierself.
	# the first parameter is template we wish to useself.
	return render(request, 'rango/index.html', context=context_dict) # render the response and send it back.
	#return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>") #prev ver.
def about(request):
	# construct a dic to pass to the template engine as its contxtself.
	# note the key boldmessage should be same as {{ x }} from the templateself.
	context_dict = {'boldmessage': "Yip, Sip, Pip, Dip, Hip, Pick!"}
	return render(request, 'rango/about.html', context=context_dict)
	#return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")
def show_category(request, category_name_slug):
	#a dictionary to pass to rendering engine
	context_dict = {}

	try:
		#return a one model sentance or raise an exception.
		category = Category.objects.get(slug = category_name_slug)

		#retrieve all of the associated pages, filter() will return a list of page objects or empty
		pages = Page.objects.filter(category=category)

		#add results list to template context under the name of pages
		context_dict['pages'] = pages
		#add category object from database to template context to verify its existence.
		context_dict['category'] = category
	except Category.DoesNotExist:
		#if could not find specified cat, do nothing, template display "no category" for us.
		context_dict['category'] = None
		context_dict['pages'] = None

	#render and return to client
	return render(request, 'rango/category.html', context_dict)

def add_category(request):
	form = CategoryForm()

	#a http post?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		#check if provided form valid
		if form.is_valid():
			#save new cat to database
			category = form.save(commit=True)
			print(category, category.slug)
			#saved, so give ok message
			#most recent cat added is on index page, thus take user back to index
			return index(request)
		else:
			#form contained errors, print to terminal.
			print(form.errors)
	#will handle the bad form, new form, or no form supplied cases.
	#render the form with error messages (if any)
	return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
	try:
		Category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		Category = None
	
	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if Category:
				page = form.save(commit=False)
				page.category = Category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else:
			print(form.errors)
	
	context_dict = {'form':form, 'category': Category}
	return render(request, 'rango/add_page.html', context_dict)