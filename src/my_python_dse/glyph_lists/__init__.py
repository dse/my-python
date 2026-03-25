__all__ = ["AGL", "COMBINED_GLYPH_LIST"]

from glyph_lists.agl import AGL
from glyph_lists.aglfn import AGLFN
from glyph_lists.cp437 import CP437
from glyph_lists.mes_1 import MES_1
from glyph_lists.mes_2 import MES_2
from glyph_lists.mes_3b import MES_3B
from glyph_lists.secs import SECS
from glyph_lists.w1g import W1G
from glyph_lists.wgl4 import WGL4
from glyph_lists.zapf_dingbats import ZAPF_DINGBATS

COMBINED_GLYPH_LIST = sorted(list(set([
    *AGL,
    *AGLFN,
    *CP437,
    *MES_1,
    *MES_2,
    *MES_3B,
    *SECS,
    *W1G,
    *WGL4,
    *ZAPF_DINGBATS
])))
