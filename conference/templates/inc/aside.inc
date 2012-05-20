{% if states.conference_ended %}

    <p><small>19 мая в&nbsp;Санкт-Петербурге прошла конференция, посвященная юзабилити и&nbsp;проектированию пользовательского взаимодействия.</small></p>

    <p><small>Уже опубликованы презентации докладов, а так же  <a href="http://www.facebook.com/media/set/?set=oa.344384208963349&type=1">фотографии с конференции</a>. В ближайшее время будут опубликованы видеозаписи докладов.</small></p>

{% else %}

    {% if states.registration_is_active %}

        <p><a href="/registration/" class="btn btn-signup btn-primary btn-large">Принять участие</a>

        <small>Участие бесплатное.<br />
        Количество мест ограничено.</small>
        Приём заявок прекращается {{ dates.registration_end|date:"d.m в H:i" }}
        </p>
        
    {% else %}

        <p><small>Приём заявок на участие в конференции завершён<br />
        Вы сможете присоединиться к онлайн-трансляции. Трансляция начнётся в 12:30 на нашем сайте.</small></p>

    {% endif %}

{% endif %}

{% include "inc/btn-share.inc" %}