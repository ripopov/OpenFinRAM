import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from mapped_verilog_to_spice import convert


class ControllerConversionTest(unittest.TestCase):
    def test_device_free_controller_is_rejected(self):
        filler = {"type": "FILLER_ASAP7_75t_R", "connections": {}}
        for cells in ({}, {"filler": filler}):
            with self.subTest(cells=cells):
                design = {"modules": {"ctrl_decode": {"ports": {}, "cells": cells}}}
                with self.assertRaisesRegex(RuntimeError, "no electrical instances"):
                    convert(design, "")


if __name__ == "__main__":
    unittest.main()
