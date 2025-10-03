from avesterra import AvEntity, AvCategory, AvContext
import avesterra.avial as av
from build.lib.avesterra import AvAuthorization, AvClass


def create_control_surface(
    name: str,
    outlet: AvEntity,
    auth: AvAuthorization
) -> AvEntity:
    e: AvEntity = av.create_entity(
        name=name,
        key=name.lower().replace(" ", "_"),
        context=AvContext.TECHNOLOGY,
        category=AvCategory.OBJECT,
        klass=AvClass.SUBSYSTEM,
        authorization=auth
    )
    av.connect_method(
        entity=e,
        outlet=outlet,
        presence=1,
        authorization=auth
    )
    return e

