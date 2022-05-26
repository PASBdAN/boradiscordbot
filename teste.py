'''from database.client import Client

client = Client()
client.tb_name = 'Users'
# client.insert(id=1234,name='Flakesu')

from datetime import datetime, timezone

dt = datetime.now(timezone.utc)

# client.delete(id=1234)

# client.insert(id=1234,name='Flakesu',created_at=dt)
client.tb_name = 'Guilds'
print(client.select('prefix'))


client.tb_name = 'Users'
print(client.select())
client.update_by_id(id=177802769611227136, created_at = datetime.now(timezone.utc))
print(client.select())'''