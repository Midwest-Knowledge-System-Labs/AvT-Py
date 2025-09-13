import avesterra
from avesterra import AvEntity, AvialModel, AvAuthorization
import avesterra.avial as av

avesterra.initialize(
    server="origin.midwksl.net",
    directory="./Certificates"
)

model = AvialModel.from_interchange(av.retrieve_entity(entity=AvEntity.from_str("<37|1|100077>"), authorization=AvAuthorization("0c0d0215-9859-4c3f-a107-65b632c1ac23")))

print(model.attributions)
for attribution in model.attributions:
    print(attribution)

avesterra.finalize()