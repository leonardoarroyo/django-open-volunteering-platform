import pytz
from django.db.models import Q
from datetime import datetime

def filter_public_transactions(qs, params):
    start_date = params.get('start_date', 0)
    end_date = params.get('end_date', 0)
    query = params.get('query', None)

    if start_date:
        start = datetime.utcfromtimestamp(int(start_date)).replace(tzinfo=pytz.utc)
        qs = qs.filter(date_created__gte=start)

    if end_date:
        end = datetime.utcfromtimestamp(int(end_date)).replace(tzinfo=pytz.utc)
        qs = qs.filter(date_created__lte=end)

    if query:
        filter_by_amount = False
        try:
            filter_by_amount = int(query)
        except ValueError:
            pass

        if filter_by_amount:
            amount = filter_by_amount
            qs = qs.filter(
                amount__contains=amount
            )
        else:
            qs = qs.filter(
                Q(user__name__icontains=query)
                | Q(user__users_userprofile_profile__full_name__icontains=query)
            )

    return qs
