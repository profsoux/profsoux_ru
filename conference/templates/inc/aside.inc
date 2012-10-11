{% if states.conference_ended %}

    <p class="small">19 мая в&nbsp;Санкт-Петербурге прошла конференция, посвященная юзабилити и&nbsp;проектированию пользовательского взаимодействия.</p>

    <p class="small">Уже опубликованы презентации докладов, а так же  <a href="http://www.facebook.com/media/set/?set=oa.344384208963349&type=1" target="_blank">фотографии с конференции</a>. Видеозаписи докладов вы можете посмотреть на <a href="https://vimeo.com/channels/profsoux2012" target="_blank">нашем канале</a>.</p>

    <p class="small">Спасибо всем, кто <a href="http://profsoux.ru/organizers/">сделал эту конференцию</a>!</p>

    <p><a href="/registration/future/" class="btn btn-signup btn-primary btn-large">Хочу принять участие в&nbsp;ProfsoUX 2013</a>

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