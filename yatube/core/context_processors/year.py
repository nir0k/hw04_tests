import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    year = (datetime.date.today()).year
    return {
        'year': year,
    }
