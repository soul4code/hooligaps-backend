import datetime

import pytest

from models import History
from deepdiff import DeepDiff

history_data = [
    {
        'date': datetime.date.fromisoformat('2025-05-01'),
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
    },
    {'date': datetime.date.fromisoformat('2025-05-09'), 'first_name': 'John', 'last_name': 'Smith'},
    {'date': datetime.date.fromisoformat('2025-05-11'), 'first_name': 'John', 'last_name': 'Doe'},
    {'date': datetime.date.fromisoformat('2025-05-12'), 'first_name': 'John', 'last_name': 'Smith'},
    {
        'date': datetime.date.fromisoformat('2025-05-01'),
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
    },
    {'date': datetime.date.fromisoformat('2025-05-10'), 'first_name': 'John', 'last_name': 'Smith'},
    {'date': datetime.date.fromisoformat('2025-05-10'), 'first_name': 'John', 'last_name': 'Doe'},
    {'date': datetime.date.fromisoformat('2025-05-12'), 'first_name': 'John', 'last_name': 'Smith'},
    {'date': datetime.date.fromisoformat('2025-05-10'), 'first_name': 'John', 'last_name': 'Smith'},
    {'date': datetime.date.fromisoformat('2025-05-11'), 'first_name': 'Jane', 'last_name': 'Doe'},
    {'date': datetime.date.fromisoformat('2025-05-12'), 'first_name': 'Jane', 'last_name': 'Smith'},
    {'date': datetime.date.fromisoformat('2025-05-13'), 'first_name': 'John', 'last_name': 'Smith'},
    {'date': datetime.date.fromisoformat('2025-05-14'), 'first_name': 'John', 'last_name': 'Smith'},
    {'date': datetime.date.fromisoformat('2025-05-15'), 'first_name': 'Jane', 'last_name': 'Doe'},
    {'date': datetime.date.fromisoformat('2025-05-16'), 'first_name': 'Jane', 'last_name': 'Smith'},
]

expected_response = [
    {'date': '2025-05-16', 'first_name': 'Jane', 'last_name': 'Smith', 'count': 1},
    {'date': '2025-05-15', 'first_name': 'Jane', 'last_name': 'Doe', 'count': 1},
    {'date': '2025-05-14', 'first_name': 'John', 'last_name': 'Smith', 'count': 6},
    {'date': '2025-05-13', 'first_name': 'John', 'last_name': 'Smith', 'count': 5},
    {'date': '2025-05-12', 'first_name': 'John', 'last_name': 'Smith', 'count': 3},
    {'date': '2025-05-12', 'first_name': 'John', 'last_name': 'Smith', 'count': 3},
    {'date': '2025-05-12', 'first_name': 'Jane', 'last_name': 'Smith', 'count': 0},
    {'date': '2025-05-10', 'first_name': 'John', 'last_name': 'Doe', 'count': 0},
    {'date': '2025-05-11', 'first_name': 'Jane', 'last_name': 'Doe', 'count': 0},
    {'date': '2025-05-10', 'first_name': 'John', 'last_name': 'Smith', 'count': 1},
]


@pytest.mark.asyncio
async def test_history_request(client, db_session):
    items = []
    for item in history_data:
        items.append(History(**item))
    db_session.add_all(items)
    await db_session.commit()
    response = await client.get('/history?date=2026-01-01')
    assert response.status_code == 200
    resp_parsed = [
        {
            'date': item['date'],
            'first_name': item['first_name'],
            'last_name': item['last_name'],
            'count': item['count'],
        }
        for item in response.json()['items']
    ]
    diff = DeepDiff(resp_parsed, expected_response, ignore_order=True)
    assert not diff
