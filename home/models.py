from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm, Textarea, TextInput, Select

# Create your models here.
class Setting(models.Model):

	STATUS = (
		('True', 'True'),
		('False', 'False'),
	)
	title = models.CharField(max_length=150)
	keywords = models.CharField(max_length=350)
	description = models.CharField(max_length=350)
	address = models.CharField(blank=True, max_length=150)
	company = models.CharField(blank=True, max_length=150)
	phone = models.CharField(blank=True, max_length=15)
	fax = models.CharField(blank=True, max_length=20)
	email = models.CharField(blank=True, max_length=50)
	smtpserver = models.CharField(blank=True, max_length=50)
	smtpemail = models.CharField(blank=True, max_length=50)
	smtppassword = models.CharField(blank=True, max_length=50)
	smtpport = models.CharField(blank=True, max_length=50)
	icon = models.ImageField(blank=True)
	facebook = models.CharField(blank=True, max_length=50)
	instagram = models.CharField(blank=True, max_length=50)
	twitter = models.CharField(blank=True, max_length=50)
	aboutus = RichTextUploadingField(blank=True)
	contact = RichTextUploadingField(blank=True)
	references = RichTextUploadingField(blank=True)
	status = models.CharField(max_length=10, choices=STATUS)

	create_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

class ContactMessage(models.Model):
	STATUS = (
		('New', 'New'),
		('Read', 'Read'),
		('Closed', 'Closed'),
	)

	name = models.CharField(blank=True, max_length=30)
	email = models.CharField(blank=True, max_length=50)
	subject = models.CharField(blank=True, max_length=50)
	message = models.TextField(blank=True, max_length=500)
	status = models.CharField(max_length=10, choices=STATUS, default='New')
	ip = models.CharField(blank=True, max_length=30)
	note = models.CharField(blank=True, max_length=100)
	create_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class ContactForm(ModelForm):
	class Meta:
		model = ContactMessage
		fields = ['name', 'email', 'subject', 'message']
		widgets = {
			'name' : TextInput(attrs={'class': 'input','placeholder':'Name & Surname'}),
			'subject' : TextInput(attrs={'class': 'input','placeholder':'Subject'}),
			'email' : TextInput(attrs={'class': 'input','placeholder':'Email Address'}),
			'message' : Textarea(attrs={'class': 'input','placeholder':'Your Message','rows':'5'}),
		}

class FAQ(models.Model):
	STATUS = (
			('True', 'True'),
			('False', 'False'),
	)
	ordernumber = models.IntegerField()
	question = models.CharField(max_length=150)
	answer = RichTextUploadingField()
	status = models.CharField(max_length=10, choices=STATUS)
	create_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.question

