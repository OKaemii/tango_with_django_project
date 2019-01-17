from django.shortcuts import render
from django.http import HttpResponse
# importing catergory model
from rango.models import Category

def index(request):
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary
	# that will be passed to the template engine.
	# the "-" in "likes" tells it that we want it in descending order, and [:5] will return the first five.
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list}
	# contruct a dic to pass to the template engine as its contxtself.
	# note the key boldmessage shld be same as {{ x }} from the templateself.
	#context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	# return a rendered reponse to send to the clientself.
	# using shortcuts function to make life easierself.
	# the first parameter is template we wish to useself.
	return render(request, 'rango/index.html', context=context_dict) # render the response and send it back.
	#return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>") #prev ver.
def about(request):
	# contruct a dic to pass to the template engine as its contxtself.
	# note the key boldmessage shld be same as {{ x }} from the templateself.
	context_dict = {'boldmessage': "Yip, Sip, Pip, Dip, Hip, Pick!"}
	return render(request, 'rango/about.html', context=context_dict)
	#return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")
