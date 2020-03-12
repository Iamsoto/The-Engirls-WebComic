from django.shortcuts import render
from comics.models import ComicPanel
from blog.models import Post
from .models import Comment, Comment_Like
from .forms import CommentForm, ReplyForm
from django.http import HttpResponse, HttpResponseBadRequest, Http404, JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# comments/blog/blog_pk/page
def view_post_comments(request, post_pk=-1, page=1):
	comments_paginated = []

	try:
		p = Post.objects.all().get(pk=post_pk)
	except ObjectDoesNotExist as e:
		print("fuck") 
		raise Http404

	if request.method == 'POST' and request.user.is_authenticated:
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.Post = p
			# Save the comment to the database
			new_comment.user = request.user

			new_comment.save()

			return HttpResponse("Success")
		else:
			if settings.DEBUG:
				print("Comment form is not valid! HACKER!!! HACKKERRRR!")
			return HttpResponseBadRequest("bad request processing comment")
	
	if not request.user.is_authenticated:
		return HttpResponseForbidden("Cannot post comment without login")
		
	comments = p.post_comments.all().order_by("-created_on")

	# Show 5 per page
	paginator = Paginator(comments, 10)

	try:
		comments_paginated = paginator.page(page)
	except PageNotAnInteger:
		comments_paginated = paginator.page(1)
	except EmptyPage:
		comments_paginated = paginator.page(paginator.num_pages)
	except Exception as e:
		print(e)

	return render(request, "comments/comments.html", context = {'comments': comments_paginated } );	


# View the replies in a comment
def view_conversations(request, comment_pk=-1):
	reply_form = None 
	replies = []

	try:
		comment = Comment.objects.all().get(pk=comment_pk)
	except ObjectDoesNotExist as e:
		raise Http404

	if request.method == 'GET':
		reply_form = ReplyForm()
		replies = comment.comment_comments.all()

		return render(request, "comments/replies.html", context = {'replies':replies, 'reply_form': reply_form})

	if request.method == 'POST' and request.user.is_authenticated:
		reply_form = ReplyForm(request.POST)
		if reply_form.is_valid():
			new_reply = reply_form.save(commit=False)
			new_reply.Comment = comment 
			new_reply.user = request.user 
			new_reply.save()

			# On success 
			return HttpResponse("Successfully created a new reply!") 

		# If form is not valid
		else:
			return HttpResponseBadRequest("Issu processing reply")

	# If user is not authenticated
	if not request.user.is_authenticated:
		return HttpResponseForbidden("Cannot post comment without login")




# comments/comics/comic_pk/page
def view_comic_comments(request, comic_pk =-1, page=1):
	comments_paginated = []


	try:
		cp = ComicPanel.objects.all().get(pk=comic_pk)
	except ObjectDoesNotExist as e: 
		raise Http404

	if request.method == 'POST' and request.user.is_authenticated:

		comment_form = CommentForm(request.POST)
		if settings.DEBUG:
			print(comment_form.errors)
		if comment_form.is_valid():
			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.ComicPanel = cp
			# Save the comment to the database
			new_comment.user = request.user

			new_comment.save()

			return HttpResponse("Success!")

		else:
			if settings.DEBUG:
				print("Comment form is not valid! HACKER!!! HACKKERRRR!")
			return HttpResponseBadRequest("bad request processing comment")

	if not request.user.is_authenticated:
		return HttpResponseForbidden("Cannot post comment without login")

	comments = cp.comic_panel_comments.all().order_by("-created_on")

	# Show 5 per page
	paginator = Paginator(comments, 10)

	try:
		comments_paginated = paginator.page(page)
	except PageNotAnInteger:
		comments_paginated = paginator.page(1)
	except EmptyPage:
		comments_paginated = paginator.page(paginator.num_pages)
	except Exception as e:
		print(e)

	return render(request, "comments/comments.html", context = {'comments': comments_paginated } );
