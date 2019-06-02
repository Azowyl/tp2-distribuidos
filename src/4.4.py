import pybgpstream
import pprint

time_init = "2015-04-29"
time_end = "2015-04-29 00:01"

collector = 'route-views.saopaulo' # route-views.chicago

target_as = 262907 # 27747 (Telecentro)

stream = pybgpstream.BGPStream(
    from_time=time_init ,
    until_time=time_end ,
    filter = "type ribs and collector %s and path %s" % (
        collector,
        target_as
    )
)

rib = dict()

for elem in stream:
    if elem.type == 'R': # rib type
        rib[elem.fields["prefix"]] = elem.fields

for rib_elem in rib.values():
    pprint.pprint(rib_elem)
