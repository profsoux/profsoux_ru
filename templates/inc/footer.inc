    <footer id="footer">
        <nav class="container">
            <div class="row">
                {% if event.show_programm %}
                <div class="span3">
                    <h3>Что будет?</h3>
                    <p><a href="/schedule/">Программа конференции</a></p>
                </div>
                {% endif %}
                {% if counts.speakers or counts.participants %}
                <div class="span3">
                    <h3>Кто пойдёт?</h3>
                    <ul>
                        {% if counts.speakers %}
                        <li><a href="/speakers/">Докладчики</a></li>
                        {% endif %}
                        {% if counts.participants %}
                        <li><a href="/people/">Участники</a></li>
                        {% endif %}
                    </ul>
                </div>
                {% endif %}
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
                    <li class="facebook"><a class="ico hide-text" href="https://www.facebook.com/Profsoux" title="Facebook" target="_blank">Facebook</a></li>
                    <li class="twitter"><a class="ico hide-text" href="https://twitter.com/profsoux" title="Twitter" target="_blank">Twitter</a></li>
                    <li class="linkedin"><a class="ico hide-text" href="http://www.linkedin.com/groups/ProfsoUX-4806057" title="LinkedIn" target="_blank">LinkedIn</a></li>
                    <li class="vkontakte"><a class="ico hide-text" href="http://vk.com/profsoux" title="ВКонтакте" target="_blank">ВКонтакте</a></li>
                    <li class="email"><a class="ico hide-text" href="mailto:contact@ux-spb.ru" title="Написать письмо">Написать письмо</a></li>
                </ul>
            </div>
            {% endif %}
        </nav>
    </footer>
