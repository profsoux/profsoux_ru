{% load staticfiles %}
<header id="header">
    <div class="container">
        <hgroup id="branding">
            <div class="offset4">
                <a id="logo" class="visible-desktop" href="/" title="Перейти на главную">
                    <img src="{% static "img/branding/logo_profsoux.png" %}" alt="{{ site_title }}" />
                    <time class="year">{{ event.short_name }}</time>
                </a>
                <h2 id="site-description">ProfsoUX'14<br>User Experience conference</h2>
                <p><time>April 26, 2014</time>. St. Petersburg, Russia</p>
            </div>
        </hgroup>
    </div>
</header>
