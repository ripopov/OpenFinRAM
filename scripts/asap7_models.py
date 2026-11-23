"""Model-card preparation shared by the ASAP7 characterization tools."""

from pathlib import Path


def prep_models(models: Path | None, simulator: str, workdir: Path, standin: str) -> tuple[str, str]:
    """Return (include_text, description). Adapt an ASAP7 HSPICE card for Xyce."""
    if models is None:
        return standin, "planar stand-in (NOT ASAP7-accurate)"
    if simulator == "xyce":
        # ASAP7 ships the card as HSPICE level 72.  Xyce implements several
        # BSIM-CMG versions and selects between them by `level`, so the level
        # chosen here decides which equations these parameters are run
        # against.  The card declares `version = 107` on every model -- a
        # parameter Xyce reports as unrecognised and ignores -- so 107 is the
        # level matching how the extraction was done.
        #
        # This said 110 until it was measured.  On nmos_sram at 0.7 V level 110
        # gives Ion = 52.97 uA against 57.07 uA at 107, i.e. 7.2% low.
        #
        # Correcting it moves table3's clk->Q *further* from the report's
        # reference (cell_rise -9.8% -> -12.9%, still inside the 15% gate but
        # with less room), because the level error was partly cancelling the
        # known un-extracted junction/via parasitics that make this flow read
        # fast.  Two compensating errors look like better agreement than one
        # real error does; the remaining gap now has a single documented cause.
        adapted = workdir / f"{models.stem}_xyce.pm"
        adapted.write_text(models.read_text().replace("level = 72", "level = 107"))
        return (
            f".include {adapted}",
            f"{models.name} -> Xyce BSIM-CMG L107 (real ASAP7)",
        )
    return f".include {models}", f"{models.name} (real device card)"
