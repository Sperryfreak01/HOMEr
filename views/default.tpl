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
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css">


    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

<body>

    %include nav rooms=rooms, functions=functions, settings=settings
    <div class="container">
        <div class="panel-group col-xs-12" id="Weatherpanel">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a data-toggle="collapse" data-parent="#accordion">
                          Current Weather
                        </a>
                    </h4>
                </div>
                <div class="panel-body">
                    <div class="row">
                            <div class="col-xs-1"></div>
                                <iframe id="forecast_embed" type="text/html" frameborder="0" height="245" width="100%" src="http://forecast.io/embed/#lat=33.677662&lon=-117.674959"> </iframe>
                    </div>
                </div>
            </div>
        </div>


        <div class="panel-group col-xs-6" id="accordion">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a data-toggle="collapse" data-parent="#accordion">
                          Users
                        </a>
                    </h4>
                </div>
                <div id="Userscollapse" class="panel">
                    <div class="panel-body">
                        <div class="col-xs-10">
                            %for user in users:
                            <div class="row">
                                <li><b>{{user[0]}} is at {{user[1]}}</b></li>
                            </div>
                            %end
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
        <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
        <script src="//code.jquery.com/ui/1.11.1/jquery-ui.js"></script>
        <script type='text/javascript' src="static/js/bootstrap.min.js"></script>
  </script
        </script>
  </body>
</html>

