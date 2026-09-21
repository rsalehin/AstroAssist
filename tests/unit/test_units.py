"""Round-trip tests for the astropy JSON codecs [F-CORE-004]."""

from __future__ import annotations

import astropy.units as u
import numpy as np
import pytest
from astropy.coordinates import SkyCoord
from astropy.time import Time

from astroassist.core.units import QuantityValue, SkyCoordValue, TimeValue


def test_quantity_scalar_round_trip() -> None:
    q = 4.965 * u.pc
    qv = QuantityValue.from_quantity(q)
    assert qv.unit == "pc"
    assert qv.value == pytest.approx(4.965)
    back = qv.to_quantity()
    assert back.unit == u.pc
    assert back.value == pytest.approx(4.965)


def test_quantity_array_round_trip() -> None:
    q = np.array([1.0, 2.0, 3.0]) * u.km / u.s
    qv = QuantityValue.from_quantity(q)
    assert isinstance(qv.value, list)
    back = qv.to_quantity()
    assert back.unit == (u.km / u.s)
    np.testing.assert_allclose(np.asarray(back.value), [1.0, 2.0, 3.0])


def test_quantity_json_round_trip() -> None:
    qv = QuantityValue.from_quantity(1.23 * u.mag)
    restored = QuantityValue.model_validate_json(qv.model_dump_json())
    assert restored.to_quantity().unit == u.mag
    assert restored.value == pytest.approx(1.23)


def test_skycoord_round_trip() -> None:
    c = SkyCoord(ra=154.9017 * u.deg, dec=19.8699 * u.deg, frame="icrs")
    sv = SkyCoordValue.from_skycoord(c)
    assert sv.frame == "icrs"
    assert sv.ra_deg == pytest.approx(154.9017)
    assert sv.dec_deg == pytest.approx(19.8699)
    back = sv.to_skycoord()
    assert back.ra.deg == pytest.approx(154.9017)
    assert back.dec.deg == pytest.approx(19.8699)


def test_skycoord_json_round_trip() -> None:
    sv = SkyCoordValue.from_skycoord(SkyCoord(ra=10 * u.deg, dec=-20 * u.deg))
    restored = SkyCoordValue.model_validate_json(sv.model_dump_json())
    assert restored.to_skycoord().dec.deg == pytest.approx(-20.0)


def test_time_round_trip() -> None:
    t = Time("2025-01-01T00:00:00", scale="utc")
    tv = TimeValue.from_time(t)
    assert tv.scale == "utc"
    back = tv.to_time()
    assert abs((back - t).sec) < 1e-6
