<nav id="nav-main" class="navbar navbar-fixed-top">
    <div class="navbar-inner">
        <div class="container">
            <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </a>
            <div class="nav-collapse">
                <ul class="nav">
                    {% for item in items %}
                    <li {% if item.link == path %}
                         class="active"
                        {% endif %}><a href="{{ item.link }}">{{ item.name }}</a></li> 
                    {% endfor %}                       
                </ul>
            </div><!--/.nav-collapse -->
        </div>
    </div>
</nav>