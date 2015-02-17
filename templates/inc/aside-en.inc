{% if states.conference_ended %}

    <p class="small">On {{ event.date|date:"m/d/Y" }} the great UX event was held in Saint Petersburg.</p>

    <p class="small">The Videos and Presentation slides can be found in the <a href="/speakers/">Speakers section</a>.</p>
    
    <p class="small">The Photos are at our <a href="http://www.facebook.com/Profsoux/">Facebook group</a>.</p>

    <p class="small">Many Thanks to our Guests, <a href="/partners/">Partners</a> and <a href="/organizers/">Volunteers</a>!</p>

    <p><a href="{{ registration_url }}" class="btn btn-signup btn-primary btn-large">I wish to attend &nbsp;ProfsoUX15</a>

{% else %}

    {% if states.registration = "waiting" %}
        {% if event.registration_start %}
            <p>Registration for ProfsoUX will open <nobr>{{ event.registration_start }}</nobr></p>
        {% endif %}

    {% elif states.registration = "active" %}
        <p><a href="/registration/" class="btn btn-signup btn-primary btn-large">Registration</a>

            <small>Hurry up! The places are limited.<br>Please note that the primary conference language is Russian.</small><br />
            {% if event.registration_end %}
            Registration closed
            {{ event.registration_end }}
            {% endif %}
        </p>
    {% else %}
        <p><small>Registration is closed <br />
        <a href="/online/">Watch us live</a>.</small></p>
    {% endif %}

    {% if counts.participants %}
        <p>Registered already: {{ counts.participants }}.<br /><a href="/people/">Who is coming? »</a></p>
    {% endif %}

{% endif %}

{% include "inc/btn-share-en.inc" %}
