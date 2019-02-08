from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.shortcuts import render
from django.http import HttpResponse
# importing catergory model
from rango.models import Category
from rango.models import Page

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from datetime import datetime

def index(request):
	request.session.set_test_cookie()
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary
	# that will be passed to the template engine.
	# the "-" in "likes" tells it that we want it in descending order, and [:5] will return the first five.
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list, 'pages': page_list}

	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']

	response = render(request, 'rango/index.html', context=context_dict)

	return response
	# contruct a dic to pass to the template engine as its contxtself.
	# note the key boldmessage shld be same as {{ x }} from the templateself.
	#context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	# return a rendered reponse to send to the clientself.
	# using shortcuts function to make life easierself.
	# the first parameter is template we wish to useself.
	#return render(request, 'rango/index.html', context=context_dict) # render the response and send it back.
	#return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>") #prev ver.
def about(request):
	if request.session.test_cookie_worked():
		print("TEST COOKIE WORKED!")
		request.session.delete_test_cookie()
	#print whether method is GET or POST
	print(request.method)
	#print the user name, if not logged in, then 'AnonymousUser'
	print(request.user)
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

@login_required
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

@login_required
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None
	
	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else:
			print(form.errors)
	
	context_dict = {'form':form, 'category': category}
	return render(request, 'rango/add_page.html', context_dict)

def register(request):
	#boolean to tell template true if registration succeeds.
	registered = False

	#if it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		#attempt to grab info from the raw form information.
		#need make user of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		#if the two forms are valid.
		if user_form.is_valid() and profile_form.is_valid():
			#save user's form data to the database.
			user = user_form.save()

			#hash password for security, then update the user object.
			user.set_password(user.password)
			user.save()

			#to sort out Userprofile instance.
			#since we need to set the user attributes ourselves,
			#we set commit=False. This delays saving the model
			#until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user

			#user provided a dp?
			#true, get it from input form and put it in the userprofile model
			if 'picture' in request.FILES:
				profile.pictures = request.FILES['picture']

			#now save the userprofile model instance.
			profile.save()

			#update our variable to indicate that the template
			#registration was successful.
			registered = True
		else:
			#invalid form ot forms - mistakes or soemthing else?
			#print problems to the terminal.
			print(user_form.errors, profile_form.errors)
	else:
		#not a HTTP POSt, so we render our form using two modelform instances.
		#these forms will be blank, ready for user input.
		user_form = UserForm()
		profile_form = UserProfileForm()
	
	#ender the template depending on the context.
	return render(request, 'rango/register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
	#if request HTTP POST, pull out the relevant infomation.
	if request.method == 'POST':
		#gather username and password provided by the user.
		#obtained from login form.
		#use request.POST.get('<variable>') as opposed to request.POST['<variable>']
		#the former returns none if value does not exist, latter raises an exception.
		username = request.POST.get('username')
		password = request.POST.get('password')

		#use django's machinery to attempt to see if the username/password
		#combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)

		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			#if account active
			if user.is_active:
				#if both valid and active, we can log user in.
				#send user back to homepage.
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				#an inactive account was used - no logging in!
				#return HttpResponse("Your Rango account is disabled.")
				error_msg = "Your Rango account is disabled."
				return render(request, 'rango/login.html', {'error_msg': error_msg})
		else:
			#bad login details were provided. So we can't log the user in.
			error_msg = "Invalid login details: {0}, {1}".format(username, password)
			return render(request, 'rango/login.html', {'error_msg': error_msg})
		
	#request is not HTTP POST,display the login form.
	#scenario likely to be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
	return render(request, 'rango/restricted.html', {})

#use login_required() decorator to ensure only those logged in can access the view
@login_required
def user_logout(request):
	#since we know user is logged in, we can just log them out.
	logout(request)
	#take the user back to the homepage.
	return HttpResponseRedirect(reverse('index'))

#A helper method
def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

# Updated the function definition
def visitor_cookie_handler(request):
	visits = int(get_server_side_cookie.COOKIES.get(request, 'visits','1'))

	last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

	#if > day since last visit...
	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1
		#update last visit cookie
		#response.set_cookie('last_visit', str(datetime.now()))
		request.session['last_visit'] = str(datetime.now())
	else:
		#set last visit cookie
		#response.set_cookie('last_visit', last_visit_cookie)
		request.session['last_visit'] = last_visit_cookie
	#update/set teh visits cookie
	#response.set_cookie('visits', visits)
	request.session['visits'] = visits