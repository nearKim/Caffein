import datetime

from core.models import OperationScheme


def get_latest_os():
    """
    :return: The latest OperatingScheme
    """
    return OperationScheme.objects.latest('id')


def get_os_now():
    """
    :return: OperatingScheme which designates current time. Probably not the latest one.
    """
    current_year = datetime.date.today().year
    current_semester = 1 if datetime.date.today().month in range(3, 9) else 2
    os1 = OperationScheme.objects.filter(current_year=current_year, current_semester=current_semester)
    # os2 = OperationScheme.objects.filter(current_semester=current_semester)
    # os_object = os1.intersection(os2)
    if not os1.count() == 1:
        raise ValueError('Operating table이 이상합니다. 관리자 계정에서 꼭 확인하세요!')
    return os1.first()