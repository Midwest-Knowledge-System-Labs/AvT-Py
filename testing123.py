from avesterra import invoke_entity_retry_bo, AvMethod
from avesterra import AvEntity, AvAttribute, AvAuthorization
from midwksl import avtc_init, avtc_fin

avtc_init()

auth: AvAuthorization = AvAuthorization("0c0d0215-9859-4c3f-a107-65b632c1ac24")

invoke_entity_retry_bo(
    entity=AvEntity.from_str("<37|1|102841>"),
    method=AvMethod.CREATE,
    attribute=AvAttribute.PERSON,
    presence=1,
    authorization=auth
)


avtc_fin()