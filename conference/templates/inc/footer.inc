    <footer id="footer">
        <nav class="container">
            <div class="row">
                <div class="span3">
                {% if counts.lectures %}
                    <h3>Что будет?</h3>
                    <p><a href="/schedule/">Программа конференции</a></p>
                {% else %}
                    &nbsp;
                {% endif %}
                </div>
                <div class="span3">
                {% if counts.speakers or counts.participants %}
                    <h3>Кто пойдёт?</h3>
                    <ul>
                        {% if counts.speakers %}
                        <li><a href="/speakers/">Докладчики</a></li>
                        {% endif %}
                        {% if counts.participants %}
                        <li><a href="/people/">Участники</a></li>
                        {% endif %}
                    </ul>
                {% else %}
                    &nbsp;
                {% endif %}
                </div>
                <div class="span3">
                    <h3>Где и когда?</h3>
                    <p>{{ event.date }},
                    <br />{{ event.city|safe }}, {{ event.place|safe }}</p>
                    <p><a href="/location/">Схема проезда</a></p>
                </div>
                <div class="span3">
                    <h3>Контакты</h3>
                    <p>Email: <a href="mailto:contact@ux-spb.ru">contact@ux-spb.ru</a><br />
                    Телефон: <a href="callto:+78123369344">+7 (812) 336 93 44</a></p>
                </div>
            </div>

            {% if not nosocial %}
            <div id="social">
                <ul class="clearfix">
                    <li class="facebook"><a class="ico hide-text" href="http://www.facebook.com/events/294327657291715/" title="Facebook" target="_blank">Facebook</a></li>
                    <li class="twitter"><a class="ico hide-text" href="https://twitter.com/#!/uxspb" title="Twitter" target="_blank">Twitter</a></li>
                    <li class="linkedin"><a class="ico hide-text" href="http://linkd.in/yN9ET2" title="LinkedIn" target="_blank">LinkedIn</a></li>
                    <li class="vkontakte"><a class="ico hide-text" href="http://vk.com/profsoux" title="ВКонтакте" target="_blank">ВКонтакте</a></li>
                    <li class="email"><a class="ico hide-text" href="mailto:contact@ux-spb.ru" title="Написать письмо">Написать письмо</a></li>
                </ul>
            </div>
            {% endif %}
        </nav>
    </footer>

    <script src="{{ STATIC_URL }}js/jquery.js"></script>
    <!-- <script src="{{ STATIC_URL }}js/less.js"></script> -->
    <script src="{{ STATIC_URL }}js/bootstrap.js"></script>
    <script src="{{ STATIC_URL }}js/common.js?dt=20120519"></script>
    <script type="text/javascript" src="//yandex.st/share/share.js" charset="utf-8"></script>

    <script>
        var _gaq=[['_setAccount','UA-5272530-10'],['_trackPageview']];
        (function(d,t){var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
        g.src=('https:'==location.protocol?'//ssl':'//www')+'.google-analytics.com/ga.js';
        s.parentNode.insertBefore(g,s)}(document,'script'));
    </script>
</body>
</html>