"""
Mock VCF with 5 parts with small differences
"""

from consts import *
from vcf_factory import choice_rules_factory
from vcf_factory import generator_factory
from vcf_factory import VCFData


vcf = VCFData('test.vcf')

nucleotides_gen = choice_rules_factory(values=NUCLIOTIDES)

# ===== define mandatory fields ===============================================

vcf.define_mandatory_field(CHROM, default=1, Number=1, Type=INTEGER)

vcf.define_mandatory_field(
    POS,
    generator=generator_factory(100000, 1),
    Number=1,
    Type=INTEGER
)

vcf.define_mandatory_field(ID, default='.', Number=1, Type=STRING)
vcf.define_mandatory_field(REF, nucleotides_gen, Number=1, Type=STRING)
vcf.define_mandatory_field(ALT, nucleotides_gen, Number=1, Type=STRING)

QUAL_MIN = 200.0
QUAL_MAX = 599.9
vcf.define_mandatory_field(
    QUAL, choice_rules_factory(QUAL_MIN, QUAL_MAX),
    Number=1, Type=FLOAT
)

vcf.define_mandatory_field(FILTER, default='PASS', Number=1, Type=STRING)

# ===== define INFO section ===================================================
vcf.define_info_field(
    default=".",
    ID='OID', Number='.', Type=STRING,
    Description="List of original Hotspot IDs"
)

INFO_OPOS_MIN = 800000
INFO_OPOS_MAX = 890000
vcf.define_info_field(
    choice_rules_factory(INFO_OPOS_MIN, INFO_OPOS_MAX),
    ID='OPOS', Number='.', Type=INTEGER,
    Description="List of original allele positions"
)

vcf.define_info_field(
    nucleotides_gen,
    ID='OREF', Number='.', Type=STRING,
    Description="List of original reference bases"
)

vcf.define_info_field(
    nucleotides_gen,
    ID='OALT', Number='.', Type=STRING,
    Description="List of original variant bases"
)

INFO_AO_MIN = 10
INFO_AO_MAX = 200
vcf.define_info_field(
    choice_rules_factory(INFO_AO_MIN, INFO_AO_MAX),
    ID='AO', Number='A', Type=INTEGER,
)

INFO_ADP_MIN = 20
INFO_ADP_MAX = 200
vcf.define_info_field(
    choice_rules_factory(INFO_ADP_MIN, INFO_ADP_MAX),
    ID='ADP', Number='A', Type=INTEGER,
)


INFO_DP_MIN = 10
INFO_DP_MAX = 200
vcf.define_info_field(
    choice_rules_factory(INFO_DP_MIN, INFO_DP_MAX),
    ID='DP', Number=1, Type=INTEGER,
)

FR_VALUE = 'LITTLE_REASON#1'
vcf.define_info_field(default=FR_VALUE, ID='FR', Number='.', Type=STRING)

INFO_FAO_MIN = 10
INFO_FAO_MAX = 200
vcf.define_info_field(
    choice_rules_factory(INFO_FAO_MIN, INFO_FAO_MAX),
    ID='FAO', Number='A', Type=INTEGER,
)

INFO_FDP_MIN = 10
INFO_FDP_MAX = 200
vcf.define_info_field(
    choice_rules_factory(INFO_FDP_MIN, INFO_FDP_MAX),
    ID='FDP', Number=1, Type=INTEGER,
)

INFO_FWDB_MIN = -1.0
INFO_FWDB_MAX = 1.0
vcf.define_info_field(
    choice_rules_factory(INFO_FWDB_MIN, INFO_FWDB_MAX),
    ID='FWDB', Number='A', Type=FLOAT,
)

OLD_INFO_FXX_MIN = 0.0
OLD_INFO_FXX_MAX = 0.1
vcf.define_info_field(
    choice_rules_factory(OLD_INFO_FXX_MIN, OLD_INFO_FXX_MAX),
    ID='FXX', Number=1, Type=FLOAT,
)

OLD_INFO_HRUN_VALUES = [1, 2, 4]
vcf.define_info_field(
    choice_rules_factory(values=OLD_INFO_HRUN_VALUES),
    ID='HRUN', Number='A', Type=INTEGER,
)

vcf.define_info_field(default='', ID='HS', Number=0, Type=FLAG)
vcf.define_info_field(default=1, ID='LEN', Number='A', Type=INTEGER)
vcf.define_info_field(default=1, ID='NC', Number='1', Type=INTEGER)

vcf.make()

# ===== second part with new HRUN rule ========================================
NEW_INFO_HRUN_VALUES = [3, 5, 7]
vcf.change_choice_func(
    'HRUN', choice_rules_factory(values=NEW_INFO_HRUN_VALUES)
)

vcf.make()

# ===== third part with new range for the QUAL values =========================
NEW_QUAL_MIN = 600.0
NEW_QUAL_MAX = 900.0

vcf.change_choice_func(QUAL, choice_rules_factory(NEW_QUAL_MIN, NEW_QUAL_MAX))
vcf.make()

# ===== forth part with nested lists in the INFO_FXX field ====================
NEW_INFO_FXX_MIN = 0.11
NEW_INFO_FXX_MAX = 0.5
vcf.change_choice_func(
    'FXX',
    choice_rules_factory(
        start=NEW_INFO_FXX_MIN,
        finish=NEW_INFO_FXX_MAX,
        round_digits=6,
        list_size=3
    )
)
vcf.make()

# ===== fifth part with new values for FR =====================================
NEW_FR_VALUE = 'SMALL_REASON#2'
vcf.change_choice_func('FR', default=NEW_FR_VALUE)

vcf.make()


# the end: write vcf-file
vcf.write()
