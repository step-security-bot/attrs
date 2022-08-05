# SPDX-License-Identifier: MIT

import sys

import pytest

import attr
import attrs


if sys.version_info < (3, 8):
    import importlib_metadata as metadata
else:
    from importlib import metadata


@pytest.fixture(name="mod", params=(attr, attrs))
def _mod(request):
    yield request.param


class TestLegacyMetadataHack:
    def test_version(self, mod):
        """
        __version__ returns the correct version.
        """
        with pytest.deprecated_call() as ws:
            assert metadata.version("attrs") == mod.__version__

        assert (
            f"Accessing {mod.__name__}.__version__ is deprecated"
            in ws.list[0].message.args[0]
        )

    def test_description(self, mod):
        """
        __description__ returns the correct description.
        """
        with pytest.deprecated_call() as ws:
            assert "Classes Without Boilerplate" == mod.__description__

        assert (
            f"Accessing {mod.__name__}.__description__ is deprecated"
            in ws.list[0].message.args[0]
        )

    @pytest.mark.parametrize("name", ["__uri__", "__url__"])
    def test_uri(self, mod, name):
        """
        __uri__ & __url__ returns the correct project URL.
        """
        with pytest.deprecated_call() as ws:
            assert "https://www.attrs.org/" == getattr(mod, name)

        assert (
            f"Accessing {mod.__name__}.{name} is deprecated"
            in ws.list[0].message.args[0]
        )

    def test_email(self, mod):
        """
        __email__ returns Hynek's email address.
        """
        with pytest.deprecated_call() as ws:
            assert "hs@ox.cx" == mod.__email__

        assert (
            f"Accessing {mod.__name__}.__email__ is deprecated"
            in ws.list[0].message.args[0]
        )

    def test_does_not_exist(self, mod):
        """
        Asking for unsupported dunders raises an AttributeError.
        """
        with pytest.raises(
            AttributeError,
            match=f"module {mod.__name__} has no attribute __yolo__",
        ):
            mod.__yolo__
