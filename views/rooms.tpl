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
        <link href="{{webroot}}static/css/bootstrap.min.css" rel="stylesheet">


        <!-- Custom styles for this template -->
        <link href="{{webroot}}static/css/HOMEr.css" rel="stylesheet">
        <link href="{{webroot}}static/css/bootstrap-slider.css" rel="stylesheet">
        <link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/themes/smoothness/jquery-ui.css" />
        <link href="{{webroot}}static/css/toastr.css" rel="stylesheet">
        <link href="{{webroot}}static/css/font-awesome.min.css" rel="stylesheet">



        <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!--[if lt IE 9]>
          <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
          <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
        <![endif]-->
    </head>

    <body>
        %include nav webroot=webroot, rooms=rooms, functions=functions


        <div class="container">
            %for lamp in lamps:
            <div class="panel-group" id="accordion">
              <div class="panel panel-default">
                <div class="panel-heading">
                  <h4 class="panel-title">
                    <a data-toggle="collapse" data-parent="#accordion" href="#{{lamp[1]}}collapse">
                      {{lamp[0]}}
                    </a>
                  </h4>
                </div>
                <div id="{{lamp[1]}}collapse" class="panel-collapse collapse">
                  <div class="panel-body">
                      <div class="row">
                          <div class=" col-md-7">
                              <div class="row">
                                <div class="col-xs-1"></div>
                                <div class="col-xs-6 slider" id="{{lamp[1]}}" data-callback="{{lamp[1]}}-slider-result" data-value="{{lamp[2]}}" data-id="{{lamp[3]}}" data-webroot="{{webroot}}"></div>
                              </div>
                              <div class="row">
                                <br>
                                <div class="col-xs-1"></div>
                                <div class="col-xs-6">
                                    <button type="button" class="btn btn-primary btn-sm downbutton" id="{{lamp[1]}}downbutton">
                                        <span class="glyphicon glyphicon-minus"></span>
                                    </button>
                                    <button type="button" class="btn btn-primary btn-sm upbutton" id="{{lamp[1]}}upbutton">
                                        <span class="glyphicon glyphicon-plus"></span>
                                    </button>
                                    <b>&nbsp&nbsp&nbspCurrent Brightness: </b><span class="{{lamp[1]}}-slider-result">0</span>%
                                </div>
                              </div>
                          </div>
                          <div class=" col-md-5">
                            <button type="button" class="btn btn-primary btn-lg offButton" id="{{lamp[1]}}offButton">
                                <span class="fa fa-circle-o fa-2x"></span>
                                <br>OFF
                            </button>
                            <button type="button" class="btn btn-primary btn-lg onButton" id="{{lamp[1]}}onButton">
                                <span class="fa fa-sun-o fa-2x"></span>
                                <br>ON
                            </button>
                            <button type="button" class="btn btn-primary btn-lg nightButton" id="{{lamp[1]}}  nightButton">
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
        <script type='text/javascript' src="{{webroot}}static/js/bootstrap.min.js"></script>
        <script type='text/javascript' src="{{webroot}}static/js/toastr.js"></script>
        <script type='text/javascript' src="{{webroot}}static/js/slider.js"></script>
    </body>
</html>

