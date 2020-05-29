% include('header.tpl')
<nav>
	<a href="/">Home</a>
	<a href="/blog">Blog</a>
</nav>
<hr>
<main>
	<article>
		<h2>
			{{ title }}
		</h2>
		{{ !body }}
	</article>
</main>
<hr>
<div id="post">
	<h3>Post a comment:</h3>
	<form action="/blog/{{ id }}" method="post">
		<input type="text" name="username"> <br>
		<textarea name="comment"></textarea> <br>
		<input type="submit" name="submit" value="Post comment">
	</form>
</div>
<br>
<div id="comments">
	<h3>Comments:</h3>
	% for comment in comments:
		<article class="comment">
			<h3 id="username">{{ comment.user }}</h3>
			{{ comment.comment }}
		</article>
	% end
</div>
<hr>
% include('footer.tpl')

