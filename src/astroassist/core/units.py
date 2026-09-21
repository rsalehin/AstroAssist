"""JSON-serializable wrappers for astropy scientific types [F-CORE-004].

Rule: no physical number without a unit. These Pydantic models are how ``Quantity``,
``SkyCoord`` and ``Time`` cross the wire (API, storage, LLM context) and come back as
genuine astropy objects. Unit conversion is always done by astropy, never by hand.
"""

from __future__ import annotations

from typing import Any

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.time import Time
from pydantic import BaseModel, Field


class QuantityValue(BaseModel):
    """A scalar or array ``astropy.units.Quantity`` as ``{value, unit}``."""

    value: float | list[float]
    unit: str = Field(description="astropy unit string, e.g. 'pc', 'km / s', '' for dimensionless")

    @classmethod
    def from_quantity(cls, quantity: u.Quantity) -> QuantityValue:
        raw = quantity.value
        value: float | list[float] = (
            float(raw) if np.ndim(raw) == 0 else [float(x) for x in np.atleast_1d(raw).ravel()]
        )
        return cls(value=value, unit=quantity.unit.to_string())

    def to_quantity(self) -> u.Quantity:
        return u.Quantity(self.value, u.Unit(self.unit))


class SkyCoordValue(BaseModel):
    """A sky position normalized to degrees with an explicit frame and optional epoch."""

    ra_deg: float
    dec_deg: float
    frame: str = "icrs"
    epoch: str | None = None

    @classmethod
    def from_skycoord(cls, coord: SkyCoord) -> SkyCoordValue:
        icrs = coord.icrs
        epoch: str | None = None
        obstime = getattr(coord, "obstime", None)
        if obstime is not None:
            epoch = str(obstime)
        return cls(
            ra_deg=float(icrs.ra.deg),
            dec_deg=float(icrs.dec.deg),
            frame="icrs",
            epoch=epoch,
        )

    def to_skycoord(self) -> SkyCoord:
        kwargs: dict[str, Any] = {"frame": self.frame}
        if self.epoch is not None:
            kwargs["obstime"] = self.epoch
        return SkyCoord(ra=self.ra_deg * u.deg, dec=self.dec_deg * u.deg, **kwargs)


class TimeValue(BaseModel):
    """An ``astropy.time.Time`` as ISO string + scale + format."""

    iso: str
    scale: str = "utc"
    format: str = "iso"

    @classmethod
    def from_time(cls, time: Time) -> TimeValue:
        return cls(iso=str(time.utc.iso), scale="utc", format="iso")

    def to_time(self) -> Time:
        return Time(self.iso, scale=self.scale, format=self.format)
