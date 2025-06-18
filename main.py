import avesterra
from avesterra import AvEntity

avesterra.initialize(
    server="192.168.1.251",
    directory="/AvesTerra/Certificates/meep",
)
print(avesterra.server_version(server=AvEntity(0,0,0)))

avesterra.finalize()