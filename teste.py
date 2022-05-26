from database.client import Client

client = Client('Users')
# client.insert(id=1234,name='Flakesu')

from datetime import datetime, timezone

dt = datetime.now(timezone.utc)

# client.delete(id=1234)

# client.insert(id=1234,name='Flakesu',created_at=dt)
# client.tb_name = 'Guilds'
# print(client.select('prefix'))

user_parameters = client.select('roll_count','roll_timestamp',id = 177802769611227136)
if user_parameters:
    # if user_parameters[0][0] < 5:
    #     print(True)
    print(dt, type(dt))
    print(user_parameters[0][1], type(user_parameters[0][1]))
    diff = dt - user_parameters[0][1]
    print(int(diff.total_seconds() / 60))
# client.update_by_id(id=177802769611227136, created_at = datetime.now(timezone.utc))
# print(client.select())

