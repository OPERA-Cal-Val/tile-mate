class TilesetNotSupported(Exception):
    """Dataset shortname is not supported"""


class NoTileCoverage(Exception):
    """Tiles do not have coverage over requested area"""
