import requests
from pytz import timezone
from datetime import datetime


MIDNIGHT_END = 5


def load_attempts():
    link = 'https://devman.org/api/challenges/solution_attempts/'
    api_json = requests.get(link, params={'page':1}).json()
    pages = api_json['number_of_pages']
    records = list()
    for page in range(pages):
        api_page = requests.get(link, params={'page':page+1}).json()
        records.extend(api_page['records'])
    return records


def is_midnighter(user):
    if not user['timestamp']:
        return False
    normal_time = datetime.fromtimestamp(user['timestamp'])
    user_timezone = timezone(user['timezone'])
    local_timezone = user_timezone.localize(normal_time)
    if local_timezone.hour > MIDNIGHT_END:
        return False
    return True


if __name__ == '__main__':
    attempts = load_attempts()
    midnighters = {user['username'] for user in attempts if is_midnighter(user)}
    print('Code-addictive programmers are:')
    for ind, user in enumerate(midnighters):
        print(ind+1, user)
