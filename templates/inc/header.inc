{% load staticfiles %}
<header id="header">
    <div class="container">
        <hgroup id="branding">
            <div class="offset4">
                <a id="logo" class="visible-desktop" href="/" title="Перейти на главную">
                    <img src="{% static "img/branding/logo_profsoux.png" %}" alt="{{ site_title }}" />
                    <time class="year">{{ event.short_name }}</time>
                </a>
                <h2 id="site-description">{{ event.title }}</h2>
                <p><time>{{ event.date|date:"d E (l) Y"|lower }}</time>, {{ event.city }}, {{ event.place }}</p>
            </div>
        </hgroup>
    </div>
</header>
