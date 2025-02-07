import inspect

import pytest

import numcodecs
from numcodecs.errors import UnknownCodecError
from numcodecs.zarr3_registry import get_codec


def test_all_classes_registered():
    """
    find all Codec subclasses in this repository and check that they
    have been registered.

    see #346 for more info
    """
    missing = {
        obj.codec_id
        for _, submod in inspect.getmembers(numcodecs.zarr3, inspect.ismodule)
        for _, obj in inspect.getmembers(submod)
        if (
            inspect.isclass(obj)
            and issubclass(obj, numcodecs.abc.Codec)
            and obj.codec_id not in numcodecs.zarr3_registry.codec_registry
            and obj.codec_id is not None  # remove `None`
        )
    }

    if missing:
        raise Exception(f"these codecs are missing: {missing}")  # pragma: no cover
