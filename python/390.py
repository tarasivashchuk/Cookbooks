"""New features for Python v3.9.0.

- Dictionary Unions
- Typehints
- Timezones
- Removed prefix/suffix
"""


# Dictionary unions

a = {"name": "Taras", "job": "Adventurer"}
b = {"name": "Taras", "job": "Creator"}

print(a | b) # instead of {**a, **b}
a |= b # instead of a.update(b)
print(a)


# Timezones
from datetime import datetime
from pytz import timezone
from zoneinfo import ZoneInfo

current_time = datetime.now()
print(current_time)
current_time_kiev = datetime.now().astimezone(timezone("Europe/Kiev")) # old way (requires dependency)
print(current_time_kiev)
current_time_kiev = datetime.now().astimezone(ZoneInfo("Europe/Kiev")) # new way - no dependency
print(current_time_kiev)

# Typehints

from typing import List

taras_list: List[int] = [0, 8, 0, 8] # old way requiring import
print(taras_list)

taras_list: list[int] = [0, 8, 0, 8] # new way with generic type
print(taras_list)

# Remove prefix/suffix

names = ["Mr. Taras", "Mr. Taras III"]
names = [name.removeprefix("Mr. ").removesuffix(" III") for name in names] # two new methods on string
print(names)