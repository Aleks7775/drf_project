from rest_framework.serializers import ValidationError


def validate_words(value):
    """Проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com."""
    if "youtube.com" not in value:
        raise ValidationError("Разрешенные ссылки только youtube.com")
