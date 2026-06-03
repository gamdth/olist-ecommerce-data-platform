{% macro generate_schema_name(custom_schema_name, node) %}

    {% if custom_schema_name is none %}
        main
    {% else %}
        {{ custom_schema_name | trim }}
    {% endif %}

{% endmacro %}