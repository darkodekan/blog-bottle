% include('header.tpl')
<nav>
	<a href="/">Home</a>
	<a href="/blog">Blog</a>
</nav>
  	    <hr>
<div>
		<form action="/login" method="post">
 			<label for="username">Username:</label><br>
  			<input type="text" id="username" name="username">
			<br>
 			<label for="password">Password:</label><br>
  			<input type="text" id="password" name="password">
			<br>
			<input type="submit" value="Submit">
		</form> 
</div>
		<hr>
% include('footer.tpl')
