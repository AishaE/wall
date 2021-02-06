from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from .models import User, MessagePost, CommentPost


# def index(request):
# 	return HttpResponse("I am ready to handle a request for '/'!")

def index(request):
	print("is this render request even working? ")
	return render(request, 'login.html')

#GET - User welcome page
def user_welcome (request):
	if 'user_id' not in request.session:
		return redirect ("/")
	context = {
		"all_messages" : MessagePost.objects.all()
		}
	return render(request, "user_page.html", context)

# GET - READ Method for profile page
def user_profile(request, user_id):
	if 'user_id' not in request.session:
		return redirect ("/")
		# get the user
	context={
		'this_user': User.objects.get(id=user_id)
	}
	return render(request, 'profile.html', context)

#GET - LOGOUT ?
def user_logout (request):
	request.session.flush()
	return redirect('/')


#POST : CREATE a user (i.e. register)
def create_user(request):
	print("Hi!  Can I create a user?!")
	if request.method == "GET":
		return redirect('/')
		#run the user_validator function made in models.py and receive back a dictionary
	errors = User.objects.user_validator(request.POST)
		#if the dictionary received has errors in it, reject the form, and show the error messages
		# on the template the user was on last
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
		# encrypting  password + store plaint text pw in variable
	else: 
		user_pw=request.POST['password']
		# create the hash for the password
		hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
		print(hash_pw)
		# create user object 
		new_user = User.objects.create(
			first_name=request.POST['first_name'], 
			last_name=request.POST['last_name'], 
			bday=request.POST['bday'],
			email=request.POST['email'], 
			password=hash_pw,
		)
		print(new_user)
		# storing user's id so I can track user's interactions on the website 
		request.session['user_id']= new_user.id 
		request.session['first_name'] = new_user.first_name
		request.session['last_name'] = new_user.last_name
	return redirect('/user_success')

#POST - USER SIGN_IN
def user_login(request):
	print('Is this user_login method working?')
	if request.method == 'POST':
		# query to find the user
		logged_user=User.objects.filter(email=request.POST['email'])

		if len(logged_user) > 0:
			logged_user = logged_user[0]
			print(logged_user)
			print(logged_user.password, request.POST['password'])

			if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
				request.session['user_id'] = logged_user.id 
				request.session['first_name'] = logged_user.first_name
				return redirect ('/user_success')
				# return redirect(f'/user_success/{logged_user.id}')
			else :
				messages.error(request, "Your password is incorrect.")
		else:
			messages.error(request, "Your email does not exist.")
	return redirect('/user_success')


#POST - CREATE a Message Post 
def create_content(request):
	print('Hey what happened to the create content method?!?!')
	if request.method == "POST":
		#validate data
		errors = MessagePost.objects.content_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value)
				return redirect('/user_success')
		#create message content
		else:
			MessagePost.objects.create(content=request.POST['content'],posted_by=User.objects.get(id=request.session['user_id']))
			return redirect('/user_success')
	return redirect('/')

# POST - CREATE a comment to a MessagePost
def create_comment(request, message_id):
	print("Is this method going to create a new comment? ")
	print(request.POST['comment'])
	print(MessagePost.objects.get(id=message_id))
	this_user=User.objects.get(id=request.session['user_id'])
	print(this_user)
	new_comment= CommentPost.objects.create(
		comment=request.POST['comment'],
		comment_message=MessagePost.objects.get(id=message_id),
		commented_by=this_user
	)
	return redirect('/user_success')

#POST -delete message
def delete_message(request, message_id):
	delete_message=MessagePost.objects.get(id=message_id)
	delete_message.delete()
	return redirect('/user_success')









