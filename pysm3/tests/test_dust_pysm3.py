import astropy.units as units
import numpy as np
import healpy as hp
from astropy.tests.helper import assert_quantity_allclose
from pysm3.models.dust import blackbody_ratio

import pysm3
from pysm3 import units as u
import pytest


@pytest.mark.parametrize("model_tag", ["d9"])
def test_dust_model_353(model_tag):
    freq = 353 * u.GHz

    model = pysm3.Sky(preset_strings=[model_tag], nside=2048)

    output = model.get_emission(freq)

    input_template = pysm3.models.read_map(
        "dust_gnilc/gnilc_dust_template_nside{nside}.fits".format(nside=2048),
        nside=2048,
        field=(0, 1, 2),
    )

    assert_quantity_allclose(input_template, output)


def test_d9_857():
    freq = 857 * u.GHz

    model = pysm3.Sky(preset_strings=["d9"], nside=2048)

    output = model.get_emission(freq)

    input_template = pysm3.models.read_map(
        "dust_gnilc/gnilc_dust_template_nside{nside}.fits".format(nside=2048),
        nside=2048,
        field=(0, 1, 2),
    )

    freq_ref = 353 * u.GHz
    scaling = (freq / (353 * u.GHz)) ** (1.48 - 2)
    scaling *= blackbody_ratio(freq, freq_ref, 19.6)

    assert_quantity_allclose(input_template * scaling, output, rtol=1e-6)
