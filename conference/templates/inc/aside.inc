
{% if states.registration_is_active %}

    <p><a href="/registration/" class="btn btn-signup btn-primary btn-large">Принять участие</a>

    <small>Участие бесплатное.<br />
    Количество мест ограничено.</small>
    Приём заявок прекращается {{ dates.registration_end|date:"d.m в H:i" }}
    </p>
    
{% else %}

    <p><small>Приём заявок на участие в конференции завершён<br />
        Вы сможете присоединиться к онлайн-трансляции.</small></p>

{% endif %}

{% include "inc/btn-share.inc" %}