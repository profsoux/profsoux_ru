{% if states.conference == 'ended' %}

    {% if event.short_name == '2013' %}

        <p class="small">25 апреля 2015&nbsp;г. в&nbsp;Санкт-Петербурге прошла конференция, посвященная юзабилити
        и&nbsp;проектированию пользовательского взаимодействия.</p>

        <p class="small">Все презентации, а также видеозаписи из Большого зала доступны <a href="/papers/">на страницах докладов</a>.
        Фотографии смотрите <a href="https://www.facebook.com/Profsoux">в&nbsp;группе на&nbsp;Facebook</a>.</p>

        <p class="small">Спасибо всем, кто <a href="http://profsoux.ru/organizers/">сделал эту конференцию</a>!</p>

    {% endif %}

    <p><a href="{{ registration_url }}" class="btn btn-signup btn-primary btn-large">Хочу принять участие в&nbsp;ProfsoUX 2015</a>

{% endif %}

{% if states.conference == 'waiting' %}
    <p>ПрофсоUX —&nbsp;конференция #1 для UX-профессионалов в России</p>

    {% if states.registration = "waiting" %}
        {% if event.registration_start %}
            <p>Приём заявок на участие в конференции «ProfsoUX» откроется <nobr>{{ event.registration_start }}</nobr></p>
        {% else %}
        {% endif %}
        <p><a href="https://docs.google.com/forms/d/13y6xAXjJ9J8uemzwEzVu5Fo2a5vBk4L4ddFfscTFxf8/viewform" class="btn btn-signup btn-primary btn-large">Принять участие</a></p>

    {% elif states.registration = "active" %}
        <p><a href="https://docs.google.com/forms/d/13y6xAXjJ9J8uemzwEzVu5Fo2a5vBk4L4ddFfscTFxf8/viewform" class="btn btn-signup btn-primary btn-large">Принять участие</a>

            <small>Торопитесь! Количество мест ограничено.</small><br />
            {% if event.registration_end %}
            Приём заявок прекращается
            {{ event.registration_end }}
            {% endif %}
        </p>
    {% else %}
        <p><small>Приём заявок на участие в конференции завершён<br />
            Вы сможете присоединиться к <a href="/online/">онлайн-трансляции</a>.</small></p>
    {% endif %}

    {% if counts.participants %}
        <p>Уже идут: {{ counts.participants }}. <a href="/people/">Кто идёт? »</a></p>
    {% endif %}

{% endif %}

{% if states.conference == 'in_progress' %}
    <p class="small">Регистрация закрыта. </p>

    <p class="small">Начало трансляции&nbsp;&mdash; 25&nbsp;апреля в&nbsp;11:30. <a href="/online/">Смотреть онлайн-трансляцию</a></p>
{% endif %}

{% include "inc/btn-share.inc" %}
