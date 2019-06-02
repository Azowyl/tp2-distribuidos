import pybgpstream

time_init = '2018-07-30'
time_end = '2018-07-30 00:00:01'

collector = 'route-views.saopaulo'  # route-views.chicago

stream = pybgpstream.BGPStream(
    from_time=time_init,
    until_time=time_end,
    filter='type ribs and collector %s' % (
        collector
    )
)

as_numbers_per_prefix = {}


def dest_as_number(elem):
    return elem.fields['as-path'].split(' ')[-1]


def prefix(elem):
    return elem.fields['prefix']


element_count = 0
for element in stream:
    element_count += 1
    as_numbers = as_numbers_per_prefix.get(prefix(element), set())
    as_numbers_per_prefix[prefix(element)] = as_numbers.union({dest_as_number(element)})

# TODO: obtener datos de este momento
# https://www.manrs.org/2019/05/public-dns-in-taiwan-the-latest-victim-to-bgp-hijack/
# o de cualquier otro incidente (hay lista en las referencias de wikipedia)
# https://en.wikipedia.org/wiki/BGP_hijacking#Public_incidents
# ver por que es tan comun encontrar prefijos que corresponden a mas de 1 as_number
print(element_count)
print(
    {prefix: as_numbers for prefix, as_numbers in as_numbers_per_prefix.iteritems() if len(as_numbers) != 1}
)
