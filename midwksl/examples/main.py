from dotenv import load_dotenv, find_dotenv
from orchestra.orchestra_adapter import OrchestraAdapter
import avesterra as av
from orchestra.adapter_interface import ValueType

load_dotenv(find_dotenv())

adapter = OrchestraAdapter(
    version="0.0.0",
    description="",
    adapting_threads=4,
    socket_count=8,
)
av.av_log.info(f"Starting with {adapter._version=}")

@adapter.route("Healthcheck")
@adapter.method(av.AvMethod.NULL)
@adapter.value_out(value_type=ValueType.null())
def healthcheck() -> av.AvValue:
    """Used to ping the adapter and check if it is healthy"""
    return av.NULL_VALUE

adapter.run()