% include('header.tpl')
<nav>
	<a href="/">Home</a>
	<a href="/blog">Blog</a>
</nav>
	<hr>
	<div style="margin-bottom: 40px;">
		% if admin:
			<a href="/submit">Submit</a>
			<a href="/logout" style="margin-bottom: 40px;">Logout</a>
		%  else:
			<a href="/login" style="margin-bottom: 40px;">Login</a>
		% end
	</div>
	% for i in range(len(article_list)):
		<article class="article_list">
			<p>{{ article_list[i].date }}</p>
			<h2><a href="/blog/{{ article_list[i].id }}">{{ article_list[i].title }}</a></h2>
		% if admin:
			<a href="/delete/{{ article_list[i].id }}" onclick="return confirm('Are you sure you want to delete this article?');">Delete</a>
			<a href="/update/{{ article_list[i].id }}">Update</a>
		% end
		</article>
			
	% end
	<hr>
% include('footer.tpl')
