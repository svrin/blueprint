<!DOCTYPE html>
<html lang="{{ handler.locale.code }}" {% block html_attr %}{% end %}>
    <head>
        {% block head %}
            <title>{% if handler.caption %}{{ handler.caption }}{% end %}</title>
        {% end %}

        <base href="{{ request.protocol + "://" + request.host }}"/>

        <meta charset="UTF-8">

        <script src="{{ request.protocol }}://cdnjs.cloudflare.com/ajax/libs/require-jquery/0.25.0/require-jquery.min.js"
                type="application/javascript"></script>
        <script src="{{ request.protocol }}://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.0.0/js/bootstrap.min.js"
                type="application/javascript"></script>
        <script src="{{ handler.request.protocol }}://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"
                type="application/javascript"></script>
    </head>
    <body {% block body_attr %}{% end %}>
    {% block body %}
        {% block content %}
            {{ content }}
        {% end %}
    {% end %}
    </body>
</html>