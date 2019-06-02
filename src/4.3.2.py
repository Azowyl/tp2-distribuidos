import pybgpstream
import pprint
from collections import OrderedDict


def remove_prepend(as_path):
    return list(OrderedDict.fromkeys(as_path))


time_init = "2017-03-01"
time_end = "2017-03-01 00:01"

collector = 'route-views.saopaulo'  # route-views.chicago

target_as = 262907  # 27747 (Telecentro)

stream = pybgpstream.BGPStream(
    from_time=time_init,
    until_time=time_end,
    filter="type ribs and collector %s and path %s" % (
        collector,
        target_as
    )
)

providers = set()
for elem in stream:
    if int(elem.fields["as-path"].split(' ')[-1]) == target_as:
        as_path = remove_prepend(elem.fields["as-path"].split(' '))
        if len(as_path) > 1:
            providers.add(as_path[-2])  # provider

pprint.pprint(providers)
