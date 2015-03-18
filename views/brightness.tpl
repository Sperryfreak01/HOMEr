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


    <!-- CSS -->
    <link href="static/css/bootstrap.min.css" rel="stylesheet">
    <link href="static/css/animate.min.css" rel="stylesheet">
    <link href="static/css/font-awesome.min.css" rel="stylesheet">
    <link href="static/css/form.css" rel="stylesheet">
    <link href="static/css/calendar.css" rel="stylesheet">
    <link href="static/css/style.css" rel="stylesheet">
    <link href="static/css/icons.css" rel="stylesheet">
    <link href="static/css/generics.css" rel="stylesheet">





        <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!--[if lt IE 9]>
          <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
          <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
        <![endif]-->
    </head>

<body id="skin-blur-violate">
        %include nav webroot=webroot, rooms=rooms, functions=functions


        <div class="container">
            %for device in devices:
            <div class="panel-group" id="accordion">
              <div class="panel panel-default">
                <div class="panel-heading">
                  <h4 class="panel-title">
                    <a data-toggle="collapse" data-parent="#accordion" href="#{{device[1]}}collapse">
                      {{device[0]}}
                    </a>
                  </h4>
                </div>
                <div id="{{device[1]}}collapse" class="panel-collapse collapse">
                  <div class="panel-body">
                      <div class="row">
                          <div class=" col-md-7">
                              <div class="row">
                                <div class="col-xs-1"></div>
                                <div class="col-xs-6 slider" id="{{device[1]}}" data-callback="{{device[1]}}-slider-result" data-value="{{device[2]}}" data-id="{{device[3]}}" data-webroot="{{webroot}}"></div>
                              </div>
                              <div class="row">
                                <br>
                                <div class="col-xs-1"></div>
                                <div class="col-xs-6">
                                    <button type="button" class="btn btn-primary btn-sm downbutton" id="{{device[1]}}downbutton">
                                        <span class="glyphicon glyphicon-minus"></span>
                                    </button>
                                    <button type="button" class="btn btn-primary btn-sm upbutton" id="{{device[1]}}upbutton">
                                        <span class="glyphicon glyphicon-plus"></span>
                                    </button>
                                    <b>&nbsp&nbsp&nbspCurrent Brightness: </b><span class="{{device[1]}}-slider-result">0</span>%
                                </div>
                              </div>
                          </div>
                          <div class=" col-md-5">
                            <button type="button" class="btn btn-primary btn-lg offButton" id="{{device[1]}}offButton">
                                <span class="fa fa-circle-o fa-2x"></span>
                                <br>OFF
                            </button>
                            <button type="button" class="btn btn-primary btn-lg onButton" id="{{device[1]}}onButton">
                                <span class="fa fa-sun-o fa-2x"></span>
                                <br>ON
                            </button>
                            <button type="button" class="btn btn-primary btn-lg nightButton" id="{{device[1]}}  nightButton">
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

