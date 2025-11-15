<<<<<<<< HEAD:src/machinations/control_surface.py
from avesterra import AvEntity, AvCategory, AvContext
from avial import avesterra as av
from avesterra import AvAuthorization, AvClass
========
from pyks.avesterra import AvEntity, AvCategory, AvContext
from pyks import avesterra as av
from pyks.avesterra import AvAuthorization, AvClass
>>>>>>>> cdcaf9e1d0dca3f93db58b9530632296467cc5db:pyks/machinations/control_surface.py


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

