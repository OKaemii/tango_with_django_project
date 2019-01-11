from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	# contruct a dic to pass to the template engine as its contxtself.
	# note the key boldmessage shld be same as {{ x }} from the templateself.
	context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	# return a rendered reponse to send to the clientself.
	# using shortcuts function to make life easierself.
	# the first parameter is template we wish to useself.
	return render(request, 'rango/index.html', context=context_dict)
	#return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>") #prev ver.
def about(request):
	return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")
