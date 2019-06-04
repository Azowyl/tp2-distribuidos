import pybgpstream

time_init = '2019-06-03 01:00:00'
time_before_hijack = '2019-06-03 02:00:00'
time_end = '2019-06-03 03:00:00'

collector = 'route-views.chicago'

stream = {
    'before': pybgpstream.BGPStream(
        from_time=time_init,
        until_time=time_before_hijack,
        filter='type ribs and collector %s' % (
            collector
        )
    ),
    'after': pybgpstream.BGPStream(
        from_time=time_before_hijack,
        until_time=time_end,
        filter='type ribs and collector %s' % (
            collector
        )
    )
}

as_numbers_per_prefix = {
    'before': {},
    'after': {}
}


def to_binary(mask):
    _ip, length = mask.split('/')
    return ''.join([bin(int(x) + 256)[3:] for x in _ip.split('.')])[0:int(length)]


def dest_as_number(elem):
    return elem.fields['as-path'].split(' ')[-1]


def prefix(elem):
    return elem.fields['prefix']


def get_matches(_as_numbers_per_prefix, mask):
    # get pairs key:value for masks that start with the same bits as the given one (they are the same or longer)
    return {k: v for k, v in _as_numbers_per_prefix.iteritems() if mask == k[0:len(mask)]}


for key in ['before', 'after']:
    for element in stream[key]:
        try:
            binary_prefix = to_binary(prefix(element))
            as_numbers = as_numbers_per_prefix[key].get(binary_prefix, set())
            as_numbers_per_prefix[key][binary_prefix] = as_numbers.union({dest_as_number(element)})
        except ValueError:
            pass


for before_mask, before_as_numbers in as_numbers_per_prefix['before']:
    try:
        for after_mask, after_as_numbers in get_matches(as_numbers_per_prefix['after'], before_mask):
            if before_as_numbers != after_as_numbers:
                print('prefix {prefix_before} was announced by AS {as_before} '
                      'and then {prefix_after} was announced by AS {as_after}'.format(
                    prefix_before=before_mask,
                    prefix_after=after_mask,
                    as_before=before_as_numbers,
                    as_after=after_as_numbers
                ))
    except KeyError:
        pass
