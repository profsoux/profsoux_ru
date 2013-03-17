{% if states.conference_ended %}

    <p class="small">On {{ event.registration_start|date:"m/d/Y" }} the conference dedicated to usability and UX was held in Saint Petersburg.</p>

    <p class="small">Presentations and <a href="http://www.facebook.com/media/set/?set=oa.344384208963349&type=1" target="_blank">the conference photos</a> are published already. Videos will be available soon.</p>

    <p class="small">Thanks to the <a href="http://{{ event.domain }}/organizers/">conference organizers</a>!</p>

    <p><a href="{{ registration_url }}" class="btn btn-signup btn-primary btn-large">I wish to attend &nbsp;ProfsoUX14</a>

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

        <p>Speakers are encouraged to submit their proposals for presentations and workshops by 1st of April 2013.
           Presentations and workshops can be delivered in English or Russian.
           Please send your proposal to <a href="mailto:pc-chairs@ux-spb.ru"><nobr>pc-chairs@ux-spb.ru</nobr></a>.</p>
    {% else %}
        <p><small>Registration is closed <br />
        Watch us live. The live video stream will start at 11:30</small></p>
    {% endif %}

    {% if counts.participants %}
        <p>Registered already: {{ counts.participants }}.<br /><a href="/people/">Who is coming? »</a></p>
    {% endif %}

{% endif %}

{% include "inc/btn-share-en.inc" %}