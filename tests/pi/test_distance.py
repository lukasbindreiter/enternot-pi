from enternot_app.pi.distance import calculate_distance


def test_distance():
    pos1 = (14.320049, 48.338040)
    pos2 = (14.323905, 48.334953)
    # roughly 446m distance
    dist = calculate_distance(*pos1, *pos2)
    assert 446 <= dist <= 447

    # a position roughly 22km distant
    pos2 = (14.323218, 48.135432)
    dist = calculate_distance(*pos1, *pos2)
    assert 22_000 <= dist <= 23_000

