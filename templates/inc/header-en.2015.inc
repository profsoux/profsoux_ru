{% load staticfiles %}
<header id="header">
    <div class="container">
        <hgroup id="branding">
            <div class="offset4">
                <a id="logo" class="visible-desktop" href="/" title="Перейти на главную">
                    <img src="{% static "img/branding/logo_profsoux.png" %}" alt="{{ site_title }}" />
                    <time class="year">{{ event.short_name }}</time>
                </a>
                <h2 id="site-description">ProfsoUX 15<br>#1 Conference For User Experience Specialists in Russia</h2>
                <p><time>April 25, 2015</time>. Club House Centre, Saint Petersburg</p>
            </div>
        </hgroup>
    </div>
</header>
