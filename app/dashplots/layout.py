"""Plotly Dash HTML layout override."""

html_layout = """
            {% extends 'base.html' %}
            {% block app_content %}
            {% app_entry %}
            <footer>
                {% config %}
                {% scripts %}
                {% renderer %}
            </footer>
            {% endblock %}

"""