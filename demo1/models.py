from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=70)
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=70)


class Post(models.Model): 
	title = models.CharField(max_length=70)
	description = models.EmailField(max_length=200)
	content = models.CharField(max_length=500)
	creation_date = models.DateField(auto_now_add=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(models.Model):
	post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
