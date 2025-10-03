from avesterra import av_log
from avesterra.avial import *
from dotenv import find_dotenv, load_dotenv
from machinations.routable_adapter import RoutableAdapter
from orchestra.interface import ValueType

load_dotenv(find_dotenv())

adapter = RoutableAdapter(
    name="Kubernetes Adapter",
    version="1.0",
    description="A Kewl Kubernetes Adapter",
    adapting_threads=1,
    socket_count=2,
    auth=AvAuthorization("0c0d0215-9859-4c3f-a107-65b632c1ac23")
)
av_log.info(f"Starting with {adapter._version=}")


@adapter.route("Healthcheck")
@adapter.method(AvMethod.NULL)
@adapter.value_out(value_type=ValueType.null())
def healthcheck() -> AvValue:
    """
    An epic healthcheck
    :return:
    """
    return NULL_VALUE


@adapter.route("Create")
@adapter.method(AvMethod.CREATE)
@adapter.attribute(AvAttribute.PERSON)
@adapter.value_out(ValueType.entity())
@adapter.control_surface()
def create(name: str) -> AvValue:
    """
    Create a Bob
    :param name:
    :return:
    """
    return AvValue.encode_entity(
        create_entity(
            name=name,
            key=name,
            authorization=adapter.auth
        )
    )

adapter.run()
