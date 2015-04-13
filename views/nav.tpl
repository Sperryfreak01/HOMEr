<!DOCTYPE html>
<!--[if IE 9 ]><html class="ie9"><![endif]-->
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0" />
        <meta name="format-detection" content="telephone=no">
        <meta charset="UTF-8">

        <meta name="description" content="Violate Responsive Admin Template">
        <meta name="keywords" content="Super Admin, Admin, Template, Bootstrap">

        <title>HOMEr Home Automation Dashboard</title>

        <!-- CSS -->
        <link href="/static/css/bootstrap.min.css" rel="stylesheet">
        <link href="/static/css/animate.min.css" rel="stylesheet">
        <link href="/static/css/font-awesome.min.css" rel="stylesheet">
        <link href="/static/css/form.css" rel="stylesheet">
        <link href="/static/css/calendar.css" rel="stylesheet">
        <link href="/static/css/style.css" rel="stylesheet">
        <link href="/static/css/icons.css" rel="stylesheet">
        <link href="static/css/toastr.css" rel="stylesheet">



    </head>
    <body id="skin-blur-violate">

        <header id="header" class="media">
            <a href="" id="menu-toggle"></a>
            <a class="logo pull-left" href="index.html">HOMEr</a>

            <div class="media-body">
                <div class="media" id="top-menu">
                    <div class="pull-left tm-icon">
                        <a data-drawer="messages" class="drawer-toggle" href="">
                            <i class="sa-top-message"></i>
                            <i class="n-count animated">5</i>
                            <span>Messages</span>
                        </a>
                    </div>
                    <div class="pull-left tm-icon">
                        <a data-drawer="notifications" class="drawer-toggle" href="">
                            <i class="sa-top-updates"></i>
                            <i class="n-count animated">9</i>
                            <span>Updates</span>
                        </a>
                    </div>



                    <div id="time" class="pull-right">
                        <span id="hours"></span>
                        :
                        <span id="min"></span>
                        :
                        <span id="sec"></span>
                    </div>

                    <div class="media-body">
                        <input type="text" class="main-search">
                    </div>
                </div>
            </div>
        </header>

        <div class="clearfix"></div>

        <section id="main" class="p-relative" role="main">

            <!-- Sidebar -->
            <aside id="sidebar">

                <!-- Sidbar Widgets -->
                <div class="side-widgets overflow">
                    <!-- Profile Menu -->
                    <div class="text-center s-widget m-b-25 dropdown" id="profile-menu">
                        <a href="" data-toggle="dropdown">
                            <span class="profile-pic animated icon">&#61822</span>
                        </a>
                        <ul class="dropdown-menu profile-menu">
                            <li><a href="">My Profile</a> <i class="icon left">&#61903;</i><i class="icon right">&#61815;</i></li>
                            <li><a href="">Messages</a> <i class="icon left">&#61903;</i><i class="icon right">&#61815;</i></li>
                            <li><a href="">Settings</a> <i class="icon left">&#61903;</i><i class="icon right">&#61815;</i></li>
                            <li><a href="">Sign Out</a> <i class="icon left">&#61903;</i><i class="icon right">&#61815;</i></li>
                        </ul>
                        <h4 class="m-0">Malinda Hollaway</h4>
                        @malinda-h
                    </div>

                    <!-- Calendar -->
                    <div class="s-widget m-b-25">
                        <div id="sidebar-calendar"></div>
                    </div>

                    <!-- Feeds -->
                    <div class="s-widget m-b-25">
                        <h2 class="tile-title">
                           News Feeds
                        </h2>

                        <div class="s-widget-body">
                            <div id="news-feed"></div>
                        </div>
                    </div>

                    <!-- Projects -->
                    <div class="s-widget m-b-25">
                        <h2 class="tile-title">
                            Projects on going
                        </h2>

                        <div class="s-widget-body">
                            <div class="side-border">
                                <small>Joomla Website</small>
                                <div class="progress progress-small">
                                     <a href="#" data-toggle="tooltip" title="" class="progress-bar tooltips progress-bar-danger" style="width: 60%;" data-original-title="60%">
                                          <span class="sr-only">60% Complete</span>
                                     </a>
                                </div>
                            </div>
                            <div class="side-border">
                                <small>Opencart E-Commerce Website</small>
                                <div class="progress progress-small">
                                     <a href="#" data-toggle="tooltip" title="" class="tooltips progress-bar progress-bar-info" style="width: 43%;" data-original-title="43%">
                                          <span class="sr-only">43% Complete</span>
                                     </a>
                                </div>
                            </div>
                            <div class="side-border">
                                <small>Social Media API</small>
                                <div class="progress progress-small">
                                     <a href="#" data-toggle="tooltip" title="" class="tooltips progress-bar progress-bar-warning" style="width: 81%;" data-original-title="81%">
                                          <span class="sr-only">81% Complete</span>
                                     </a>
                                </div>
                            </div>
                            <div class="side-border">
                                <small>VB.Net Software Package</small>
                                <div class="progress progress-small">
                                     <a href="#" data-toggle="tooltip" title="" class="tooltips progress-bar progress-bar-success" style="width: 10%;" data-original-title="10%">
                                          <span class="sr-only">10% Complete</span>
                                     </a>
                                </div>
                            </div>
                            <div class="side-border">
                                <small>Chrome Extension</small>
                                <div class="progress progress-small">
                                     <a href="#" data-toggle="tooltip" title="" class="tooltips progress-bar progress-bar-success" style="width: 95%;" data-original-title="95%">
                                          <span class="sr-only">95% Complete</span>
                                     </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Side Menu -->
                <ul class="list-unstyled side-menu">
                    <li>
                        <a class="sa-side-home" href="/">
                            <span class="menu-item">Dashboard</span>
                        </a>
                    </li>

                    <li class="dropdown">
                        <a class="sa-side-room" href="#">
                            <span class="menu-item">Rooms</span>
                        </a>
                        <ul class="list-unstyled menu-item">
                            %for room in rooms:
                            <li><a href="{{webroot}}room/{{room[1]}}">{{room[0]}}</a></li>
                            %end
                        </ul>
                    </li>

                    <li class="dropdown">
                        <a class="sa-side-page" href="#">
                            <span class="menu-item">Devices</span>
                        </a>
                        <ul class="list-unstyled menu-item">
                            %for function in functions:
                            <li><a href="{{webroot}}view{{function[1]}}">{{function[0]}}</a></li>
                            %end
                        </ul>
                    </li>

                    <li>
                        <a class="sa-side-users" href=".html">
                            <span class="menu-item">Users</span>
                        </a>
                    </li>
                    <li>
                        <a class="sa-side-history" href="viewhistory">
                            <span class="menu-item">History</span>
                        </a>
                    </li>

                    <li class="dropdown">
                        <a class="sa-side-settings" href="#">
                            <span class="menu-item">Settings</span>
                        </a>
                        <ul class="list-unstyled menu-item">
                            <li><a href="#">User Settings</a></li>
                            <li><a href="#">Device Settings</a></li>
                            <li><a href="#">System Settings</a></li>
                        </ul>
                    </li>

            </aside>
