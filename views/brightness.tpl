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
        <link href="static/css/font-awesome.min.css" rel="stylesheet">



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
            <div class="panel-group" id="accordion">
              <div class="panel panel-default">
                <div class="panel-heading">
                  <h4 class="panel-title">
                    <a data-toggle="collapse" data-parent="#accordion" href="#{{device[0]}}collapse">
                      {{device[0]}}
                    </a>
                  </h4>
                </div>
                <div id="{{device[0]}}collapse" class="panel-collapse collapse">
                  <div class="panel-body">
                      <div class="row">
                          <div class=" col-md-7">
                              <div class="row">
                                <div class="col-xs-1"></div>
                                <div class="col-xs-6 slider" id="{{device[0]}}" data-callback="{{device[0]}}-slider-result" data-value="{{device[1]}}" data-id="{{device[2]}}"></div>
                              </div>
                              <div class="row">
                                <br>
                                <div class="col-xs-1"></div>
                                <div class="col-xs-6">
                                    <button type="button" class="btn btn-primary btn-sm downbutton" id="{{device[0]}}downbutton">
                                        <span class="glyphicon glyphicon-minus"></span>
                                    </button>
                                    <button type="button" class="btn btn-primary btn-sm upbutton" id="{{device[0]}}upbutton">
                                        <span class="glyphicon glyphicon-plus"></span>
                                    </button>
                                    <b>&nbsp&nbsp&nbspCurrent Brightness: </b><span class="{{device[0]}}-slider-result">0</span>%
                                </div>
                              </div>
                          </div>
                          <div class=" col-md-5">
                            <button type="button" class="btn btn-primary btn-lg offButton" id="{{device[0]}}offButton">
                                <span class="fa fa-circle-o fa-2x"></span>
                                <br>OFF
                            </button>
                            <button type="button" class="btn btn-primary btn-lg onButton" id="{{device[0]}}onButton">
                                <span class="fa fa-sun-o fa-2x"></span>
                                <br>ON
                            </button>
                            <button type="button" class="btn btn-primary btn-lg nightButton" id="{{device[0]}}  nightButton">
                                <span class="fa fa-moon-o fa-2x"></span>
                                <br>Night
                            </button>
                          </div>
                      </div>
                  </div>
                </div>
              </div>
            </div>
            %end
        </div>

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

