import avesterra as av
from dotenv import load_dotenv, find_dotenv
from orchestra.interface import ValueType
from adapter.routable_adapter import RoutableAdapter
from avesterra import AvValue

load_dotenv(find_dotenv())

adapter = RoutableAdapter(
    name="Echo",
    version="1.0.0",
    description="An Echo adapter",
    adapting_threads=4,
    socket_count=8,
)
av.av_log.info(f"Starting with {adapter._version=}")


@adapter.route("Healthcheck")
@adapter.method(av.AvMethod.TEST)
@adapter.value_in(value_type=ValueType.null())
@adapter.value_out(value_type=ValueType.null())
def healthcheck() -> av.AvValue:
    """Used to check if the adapter is alive and healthy"""
    return av.NULL_VALUE

@adapter.route("A really cool echo method")
@adapter.method(av.AvMethod.ECHO)
@adapter.value_in(value_type=ValueType.text())
@adapter.value_out(value_type=ValueType.text())
def echo(value: AvValue) -> av.AvValue:
    """Echoes back whatever was sent in the value field of the invoke"""
    return value

adapter.run()