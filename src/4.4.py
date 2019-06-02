import pybgpstream
import pprint
from aggregate6 import aggregate

time_init = "2015-04-29"
time_end = "2015-04-29 00:01"

collector = 'route-views.kixp' # route-views.chicago

stream = pybgpstream.BGPStream(
    from_time=time_init ,
    until_time=time_end ,
    filter = "type ribs and collector %s" % (
        collector,
    )
)

rib = dict()

for elem in stream:
    if elem.type == 'R': # rib type
        rib[elem.fields["prefix"] + elem.fields["next-hop"]] = elem.fields # remove duplicates

prefixes_by_as = dict()

for rib_elem in rib.values():
    as_origin = int(rib_elem["as-path"].split(" ")[0])
    if not as_origin in prefixes_by_as.keys():
        prefixes_by_as[as_origin] = list()
    prefixes_by_as[as_origin].append(rib_elem["prefix"])

aggregated_rib_len = 0

for prefixes in prefixes_by_as.values():
    print(prefixes)
    aggregated_rib_len += len(aggregate(prefixes))

pprint.pprint("Full RIB length: %d" % len(rib))
pprint.pprint("Aggregated RIB length: %d" % aggregated_rib_len)
