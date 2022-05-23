from google_sheet_client import client
from expiringdict import ExpiringDict

cache = ExpiringDict(max_len=100, max_age_seconds=5 * 60)

DEFAULT_TEAMLEADER = ["Михаил Кирьянов", "m.kiryanov@kodland.team"]

def get_team_leaders():
    if cache.get("teachers"):
        return cache["teachers"]

    spreadsheet_id = '1UqmI_st-d6ukUSB0TqeM5TDNQkOlAYSQ7aOaFZXrxiY'
    worksheet = 'Тлы'
    sheet = client.open_by_key(spreadsheet_id).worksheet(worksheet)

    teachers = sheet.get_all_records()
    teamleaders = [
        # Миша выставлен дефолтным
        DEFAULT_TEAMLEADER,
    ]

    print(teachers)
    for t in teachers:
        if t.get("ID") and t.get("Корп. почта"):
            teamleaders.append([t["ID"], t["Корп. почта"]])
    cache["teachers"] = teamleaders
    return cache["teachers"]

def get_team_leaders_dict():
    if cache.get("teachers_dict"):
        return cache["teachers_dict"]

    teamleaders = get_team_leaders()

    cache["teachers_dict"] = {x[0]: x[1] for x in teamleaders}
    return cache["teachers_dict"]
