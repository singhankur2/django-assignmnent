from django.shortcuts import render
from django.http import HttpResponse
from demo1.models import User
from demo1.models import Post
from demo1.models import Like
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import jwt

secret_key = "ahfjpiu4rtaew89j"
# Create your views here.
#User


@csrf_exempt
def tok(request):
	data = json.loads(request.body)
	authentication = User.objects.filter(email=data["email"]).first()
	print(authentication.id, authentication.password)
	if authentication:
		if authentication.password == data["password"]:
			token = {"id":authentication.id}
			secret_key = "ahfjpiu4rtaew89j"
			token1 = str(jwt.encode(token, secret_key, algorithm='HS256'))
			print(token1)
			return JsonResponse({"token": token1})

	else:
		return JsonResponse({'message': 'user not valid'})




@csrf_exempt
def usercreateapi(request):
	new_user_data = json.loads(request.body)
	user = User(name=new_user_data["name"], email=new_user_data["email"], password=new_user_data["password"])
	user.save()
	return JsonResponse({'message': 'Data insert successfully'})




@csrf_exempt
def userreadapi(request):
	# email = json.loads(request.body)
	userid = request.GET.get('token')
	decrypt_data = jwt.decode(userid, secret_key, algorithms='HS256')
	
	user_data = User.objects.filter(id=decrypt_data['id'])

	for data in user_data:
		r = [data.name, data.email, data.password]
	return JsonResponse({'name': data.name, 'email':data.email, 'password': data.password})



@csrf_exempt
def userupdateapi(request):
	userid = request.GET.get('token')
	decrypt_data = jwt.decode(userid, secret_key, algorithms='HS256')
	user_data = User.objects.filter(id=decrypt_data["id"]).first()

	data = json.loads(request.body)

	if data.get("name") is not None:
		user_data.name = data["name"]
	if data.get("email") is not None:
		user_data.email = data["email"]
	if data.get("password") is not None:
		user_data.password = data["password"]
	user_data.save()

	return JsonResponse({'status': "successful", 
						'msg':"user data updated"})






@csrf_exempt
def userdeleteapi(request):
	userid = request.GET.get('token')
	decrypt_data = jwt.decode(userid, secret_key, algorithms='HS256')
	user_data = User.objects.filter(id=decrypt_data["id"])
	user_data.delete()
	return HttpResponse("user deleted")




#POST

@csrf_exempt
def postcreateapi(request):
	userid = request.GET.get('token')
	decrypt_data = jwt.decode(userid, secret_key, algorithms='HS256')
	user = User.objects.filter(id=decrypt_data["id"]).first()
	post_data = json.loads(request.body)
	post = Post(title=post_data["title"], description=post_data["description"], content=post_data["content"], user_id=user)
	post.save()
	return JsonResponse({
		'post_id':post.id,
		'status': 'successful',
		'message': 'post created'})



@csrf_exempt
def postreadapi(request):
	post_data = json.loads(request.body)
	posted_data = Post.objects.filter(id__in=post_data["post_id"])
	return_like_count = request.GET.get('return_like_count')


	res = []
	for post in posted_data:
		tmp = {
			'title': post.title,
			'description': post.description,
			'content': post.content,
			'creation_date': post.creation_date,
			'user': post.user_id.name,
		}

		if return_like_count=='true':
			tmp['like_count'] = len(Like.objects.filter(post_id=post))
		res.append(tmp)
	return JsonResponse(res, safe=False)


@csrf_exempt
def postupdateapi(request):
	userid = request.GET.get('token')
	decrypt_data = jwt.decode(userid, secret_key, algorithms='HS256')
	
	data = json.loads(request.body)

	post_data = Post.objects.filter(user_id=decrypt_data["id"], id=data["post_id"]).first()


	if data.get("title") is not None:
		post_data.title = data["title"]
	if data.get("description") is not None:
		post_data.description = data["description"]
	if data.get("content") is not None:
		post_data.content = data["content"]
	if data.get("creation_date") is not None:
		post_data.creation_date = data["creation_date"]
	post_data.save()
	return JsonResponse({
		'post_id':post_data.id,
		'status': "successful", 
		'msg':"post data updated"})






@csrf_exempt
def postdeleteapi(request):
	userid = request.GET.get('token')
	decrypt_data = jwt.decode(userid, secret_key, algorithms='HS256')

	data = json.loads(request.body)
	post_data = Post.objects.filter(user_id= decrypt_data['id'], id=data["post_id"])
	post_data.delete()
	return JsonResponse({'status': 'successful',
				'message': 'your post deleted'})





#LIKE
@csrf_exempt
def likecreateapi(request):
	data = json.loads(request.body)

	post = Post.objects.filter(id=data["post_id"]).first()
	user = post.user_id
	like = Like(post_id=post, user_id=user)
	like.save()
	return JsonResponse({
		'like_id':like.id,
				'status' : 'successful',
				'msg': 'Data insert successfully'})





@csrf_exempt
def likedeleteapi(request):
	data = json.loads(request.body)
	user_data = Like.objects.filter(id=data["like_id"])
	user_data.delete()
	return JsonResponse({'status' : 'successful',
				'message': 'unlike post'})