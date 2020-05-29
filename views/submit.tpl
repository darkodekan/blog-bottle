% include('header.tpl')
<nav>
	<a href="/">Home</a>
	<a href="/blog">Blog</a>
</nav>
	    <hr>
	<div>
		<form action="/submit" method="post">
 			<label for="Title">Title:</label><br>
		    % if update:
		 		<input type="hidden" id="update" name="command" value="update">
				<input type="hidden" id="update" name="id" value = {{ article.id }}>
				<textarea name="title" style="width:400px; height:20px;">{{ article.title }}</textarea> 
				<br>
 			 	<label for="body">Body:</label>
				<br>
				<textarea name="body" style="width:400px; height:200px;">{{ article.body }}</textarea> 
			% else:
			 	<input type="hidden" id="update" name="command" value="add">
				<textarea name="title" style="width:400px; height:20px;"></textarea> 
				<br>
 			 	<label for="body">Body:</label><br>
				<textarea name="body" style="width:400px; height:200px;"></textarea> 
			% end
			<br>
			<input type="submit" value="Submit">
	     </form> 
	</div>
	     <hr>
% include('footer.tpl')
