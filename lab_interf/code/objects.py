"""
Put celestial objects of interest and their coordinates here.

Many objects are included in pyephem already. If they are, you can include them
under the key "obj" as in the case of the Sun and the Moon.
See http://rhodesmill.org/pyephem/quick.html#bodies

Otherwise, for fixed point sources, use the keys "ra" and "dec", providing each
in radians or as a pyephem.Angle object (using ephem.hours or ephem.degrees)
See http://rhodesmill.org/pyephem/quick.html#angles
"""

import ephem


OBJECTS = {
    "sun": {"obj": ephem.Sun()},
    "moon": {"obj": ephem.Moon()},
    "m17": {"ra": ephem.hours("18:20:26"), "dec": ephem.degrees("16:10.6")},
    # Crab Nebula:
    "3C144": {"ra": ephem.hours("5:34:31.95"), "dec": ephem.degrees("22:00:51.1")},
    # Orion Nebula:
    "orion": {"ra": ephem.hours("5:35:17.3"), "dec": ephem.degrees("-05:24:28")},
    # 3C274, Virgo A:
    "m87": {"ra": ephem.hours("12:30:49.423"), "dec": ephem.degrees("12:23:28.04")},
}
