'''Common constants.'''

NUCLIOTIDES = ('A', 'C', 'G', 'T')

# vcf data columns
CHROM = 'CHROM'
POS = 'POS'
ID = 'ID'
REF = 'REF'
ALT = 'ALT'
QUAL = 'QUAL'
FILTER = 'FILTER'
INFO = 'INFO'
FORMAT = 'FORMAT'

MANDATORY_FIELDS = (CHROM, POS, ID, REF, ALT, QUAL, FILTER)

# Info-section keys
NUMBER = 'Number'
TYPE = 'Type'
DESCRIPTION = 'Description'

MANDATORY_FIELD_KEYS = (NUMBER, TYPE)
INFO_SECTION_KEYS = (ID, NUMBER, TYPE, DESCRIPTION)

# possible types in metadata
STRING = 'String'
INTEGER = 'Integer'
FLOAT = 'Float'
FLAG = 'Flag'

# count of rows in one part that make() generate
DEFAULT_VCF_CHUNK_SIZE = 100
DEFAULT_VCF_FILE_FORMAT = 'VCFv4.1'

DEFAULT_INFO_DESCRIPTION = '<DEFAULT INFO FIELD DESCRIPTION>'

# Some info fields descriptions for VCF head section
INFO_DESCRIPTION = dict(
    ADP='Average per-sample depth of bases with Phred score',
    AF='Allele frequency based on Flow Evaluator observation counts',
    AO='Alternate allele observations',
    ASP='Is Assembly specific. This is set if the variant only maps to one '
        'assembly',
    ASS='In acceptor splice site FxnCode = 73',
    CDA='Variation is interrogated in a clinical diagnostic assay',
    DP='Total read depth at the locus',
    DSS='In donor splice-site FxnCode = 75',
    FAO='Flow Evaluator Alternate allele observations',
    FDP='Flow Evaluator read depth at the locus',
    FR='Reason why the variant was filtered.',
    FRO='Flow Evaluator Reference allele observations',
    FSAF='Flow Evaluator Alternate allele observations on the forward strand',
    FSAR='Flow Evaluator Alternate allele observations on the reverse strand',
    FSRF='Flow Evaluator Reference observations on the forward strand',
    FSRR='Flow Evaluator Reference observations on the reverse strand',
    FWDB='Forward strand bias in prediction.',
    FXX='Flow Evaluator failed read ratio',
    HET='Number of samples called heterozygous-variant',
    HOM='Number of samples called homozygous-variant',
    HRUN='Run length: the number of consecutive repeats of the '
         'alternate allele in the reference genome',
    HS='Indicate it is at a hot spot',
    LEN='allele length',
    MLLD='Mean log-likelihood delta per read.',
    NS='Number of samples with data',
    PB='Bias of relative variant position in reference reads versus variant '
       'reads. Equals Mann-Whitney U rho statistic P(YX)+0.5P(Y=X)',
    PBP='Pval of relative variant position in reference reads versus variant '
        'reads.  Related to GATK ReadPosRankSumTest',
    QD='QualityByDepth as 4*QUAL/FDP (analogous to GATK)',
    RBI='Distance of bias parameters from zero.',
    REFB='Reference Hypothesis bias in prediction.',
    REVB='Reverse strand bias in prediction.',
    RO='Reference allele observations',
    SAF='Alternate allele observations on the forward strand',
    SAR='Alternate allele observations on the reverse strand',
    SRF='Number of reference observations on the forward strand',
    SRR='Number of reference observations on the reverse strand',
    SSEN='Strand-specific-error prediction on negative strand.',
    SSEP='Strand-specific-error prediction on positive strand.',
    SSSB='Strand-specific strand bias for allele.',
    STB='Strand bias in variant relative to reference.',
    STBP='Pval of Strand bias in variant relative to reference.',
    TYPE='The type of allele, either snp, mnp, ins, del, or complex.',
    U3="In 3' UTR Location is in an untranslated region (UTR). FxnCode = 53",
    U5="In 5' UTR Location is in an untranslated region (UTR). FxnCode = 55",
    VARB='Variant Hypothesis bias in prediction.',
    VC='Variation Class',
    WT='Number of samples called reference (wild-type)',
)
