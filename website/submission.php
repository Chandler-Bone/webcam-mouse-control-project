<?php
if(isset($_POST["submit"])){
	$feedback=$_POST["Name"].",".$_POST["email"].",".$_POST["comments"];
	$userfeedback=file_get_contents("feedback.txt");
	$fileFeedback=file_put_contents('feedback.txt', $feedback.PHP_EOL,FILE_APPEND);
	
}

?>
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

<link rel="stylesheet" href="style.css">

<title> Feedback </title>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
   <img src="mouse.png"> &nbsp;&nbsp;&nbsp;
        <img src="contactless.png">
 <!--  <a class="navbar-brand" href="#">Cursor movement</a> -->
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item">
        <a href="index.html" class="nav-link" href="#">Home </a>
      </li>
      <li class="nav-item active">
        <a class="nav-link" href="#">Download<span class="sr-only"></span></a>
      </li>

       <li class="nav-item">
        <a href="pricing.html" class="nav-link" href="#">Pricing</a>
      </li>
      </li>
      <li class="nav-item">
        <a href="feedback.html" class="nav-link" href="#">Feedback</a>
      </li>

       <li class="nav-item">
        <a href="about.html"class="nav-link" href="#">About</a>
      </li>

      <li class="nav-item">
        <a href="support.html"class="nav-link" href="#">Support</a>
      </li>
    </ul>
    
    <!--       <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Dropdown
        </a> -->

<!--         <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#">Action</a>
          <a class="dropdown-item" href="#">Another action</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#">Something else here</a>
        </div> --> 
<!--     <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form> -->
  </div>
</nav>

<h2>Thank you, your feedback has been received!</h2>
</body>
</html>