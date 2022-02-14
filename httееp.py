def get_spn(toponym):
    frame = toponym['boundedBy']['Envelope']
    l, b = map(float, frame['lowerCorner'].split())
    u, a = map(float, frame['upperCorner'].split())

    x = abs(l - u) / 2
    y = abs(a - b) / 2

    return f'{x},{y}'