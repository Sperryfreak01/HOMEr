<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="static/favicon.ico">

    <title>HOMEr Home Automation</title>

          <!-- Bootstrap core CSS -->
    <link href="static/css/bootstrap.min.css" rel="stylesheet">


    <!-- Custom styles for this template -->
    <link href="static/css/HOMEr.css" rel="stylesheet">
    <link href="static/css/bootstrap-slider.css" rel="stylesheet">
    <link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/themes/smoothness/jquery-ui.css" />
    <link href="static/css/toastr.css" rel="stylesheet">


    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">HOMEr</a>
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="https://mattlovett.com">Home</a></li>
            <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown">Apps <b class="caret"></b></a>
                <ul class="dropdown-menu">
                  <li><a href="https://mattlovett.com/tv">TV</a></li>
                  <li><a href="https://mattlovett.com/movies">Movies</a></li>
                  <li><a href="https://mattlovett.com/downloads">Downloads</a></li>
                </ul>
            </li>
            <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown">Rooms <b class="caret"></b></a>
                <ul class="dropdown-menu">
                  <li><a href="#">Living Room</a></li>
                  <li><a href="#">Kitchen</a></li>
                  <li><a href="#">Bedroom</a></li>
                </ul>
            </li>
            <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown">Devices <b class="caret"></b></a>
                <ul class="dropdown-menu">
                  <li><a href="/homer/viewbrightness">Lamps</a></li>
                  <li><a href="#">RGB</a></li>
                  <li><a href="#">Camera</a></li>
                </ul>
            </li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>


    <div class="container">
        %for device in devices:
        <div class="panel panel-default">
            <div class="panel-heading">
                <a data-toggle="collapse" data-parent="#accordion" href="#{{device[0]}}collapse">
                      <h2>{{device[0]}}</h2>
                 </a>
            </div>

            <div id="{{device[0]}}collapse" class="panel-collapse collapse in">
                <div class="panel-body">
                    <div class="col-lg-4 slider" id="{{device[0]}}" data-callback="{{device[0]}}-slider-result" data-value="{{device[1]}}" data-id="{{device[2]}}"></div>
                    <div class=col-lg-2">
                        <button type="button" class="btn btn-primary btn-sm" id="downbutton">
                        <span class="glyphicon glyphicon-minus"></span>
                        </button>
                        <button type="button" class="btn btn-primary btn-sm" id="upbutton">
                        <span class="glyphicon glyphicon-plus"></span>
                        </button>
                    </div>
                    <div><br></div>
                    <b>Current Brightness: </b><span class="{{device[0]}}-slider-result">0</span>%
                    </div>
            </div>
        %end
    </div><!-- /.container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/jquery-ui.min.js"></script>
        <script type='text/javascript' src="static/js/bootstrap.min.js"></script>
        <script type='text/javascript' src="static/js/toastr.js"></script>
        <script type='text/javascript' src="static/js/slider.js"></script>
  </body>
</html>

