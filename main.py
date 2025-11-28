import time

import avesterra.avial as av
from avesterra import AvAuthorization, AvEvent
from avesterra import AvCategory, AvClass

AUTH=AvAuthorization("0a1d79e4-3be9-4f49-ba0b-4d67596d39c3")

av.initialize(server="192.168.1.251")

e = av.create_entity(
    authorization=AUTH
)


print(e)

av.activate_entity(
    outlet=e,
    authorization=AUTH
)

# Enable timer functionality on outlet
av.arm_outlet_timer(
    outlet=e,
    authorization=AUTH
)

# Timer should be "armed"...nothing scheduled yet
print(av.entity_armed(
    entity=e,
    authorization=AUTH
))

# Set timer to count up to 15 seconds
av.schedule_timed_event(
    outlet=e,
    count=15,
    event=AvEvent.MESSAGE,
    authorization=AUTH
)

# Start the timer
av.start_outlet_timer(
    outlet=e,
    authorization=AUTH
)

#time.sleep(5)

# Reset's timer back to 0; timer will continue to tick though...just tick up from 0!
#av.reset_outlet_timer(
#    outlet=e,
#    authorization=AUTH
#)

# Stops timer from ticking; timer stops at elapsed...so it remembers where it stopped
#av.stop_outlet_timer(
#    outlet=e,
#    authorization=AUTH
#)

# Remove timer functionality from outlet
##av.disarm_outlet_timer(
#    outlet=e,
#    authorization=AUTH
#)

print(av.entity_armed(
    entity=e,
    authorization=AUTH
))

av.finalize()