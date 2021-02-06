from django.db import models
import re
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
	def user_validator(self, postData):
		email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		# add keys and values to errors dictionary for each invalid field
		if len(postData['first_name']) < 2 :
			errors['first_name'] = "Your first name must be more than 2 characters."
		if len(postData['last_name']) < 2:
			errors['last_name'] = "Your last name must be more than 2 characters."
		if not email_check.match(postData['email']):
			errors['email'] = "Email must be valid format."
		# just check to see if string is empty ; dont' check length of the string
		if postData['bday']== '':
			errors['bday'] = "Birthdate must be filled in."
		# check bday date against current timestamp
		date = datetime.strptime(postData["bday"], "%Y-%m-%d")  
		# ("%Y-%m-%d") %d-%B-%Y
		if date > datetime.now():
			errors['bday'] = "Birthdate cannot be in the future"
		# has the email already been registered?
		result = User.objects.filter(email=postData['email'])
		if len(result) > 0:
			errors['email'] ="Email address is already registered."
		if len(postData['password'])  < 8 :
			errors ['password'] = "Password must be at least 8 characters."
		if postData['password'] != postData['confirm_password']:
			errors ['confirm_password'] = "Password and confirm password do not match."
		return errors
	def login_validator(self, postData):
		pass

class MessagePostManager(models.Manager):
	def content_validator(self, postData):
		errors = {}
		if len(postData['content']) < 1 :
			errors['title'] = "You must provide content to your post."
		return errors


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	bday = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()


class MessagePost(models.Model):
	content = models.TextField()
	posted_by = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = MessagePostManager()


class CommentPost(models.Model):
	comment = models.TextField()
	comment_message = models.ForeignKey(MessagePost, related_name="comment_message", on_delete = models.CASCADE)
	commented_by = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	

