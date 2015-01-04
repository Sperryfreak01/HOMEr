
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
                        %for room in rooms:
                        <li><a href="/room/{{room[1]}}">{{room[0]}} </a></li>
                        %end
                    </ul>
                </li>
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">Devices <b class="caret"></b></a>
                    <ul class="dropdown-menu">
                        %for function in functions:
                        <li><a href="/view{{function[1]}}">{{function[0]}} </a></li>
                        %end

                    </ul>
                </li>
            </ul>
        </div><!--/.nav-collapse -->
    </div>
</div>
