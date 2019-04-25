"""Fabric files in VCF (Variant Call Format)
(for details see https://github.com/samtools/hts-specs).
"""

from collections import namedtuple
from datetime import date
from random import choice
from random import randint
from random import uniform
from vcf_consts import *

import os

__author__ = 'Anton Konovalov'
__version__ = '0.1'
__license__ = 'MIT'


# items of a INFO metadata
InfoItemFields = namedtuple('InfoItemFields', INFO_SECTION_KEYS)

# mandatory fields metadata
MandatoryFields = namedtuple('MandatoryFields', MANDATORY_FIELD_KEYS)


_INFO_PREFIX = 'INFO_'


def _random_int_list(start, finish, length):
    return [randint(start, finish) for _ in range(length)]


def _random_float_list(start, finish, length, round_digits):
    return [
        round(uniform(start, finish), round_digits)
        for _ in range(length)
    ]


def choice_rules_factory(start=None, finish=None, values=None,
                         **kwargs):
    """Functions factory for generate values.
    Generate random values from range[start, finish] or choice from values list
    In first case value can be list of random values.
    """
    list_size = kwargs.pop('list_size', 0)
    if start is not None and finish is not None:
        if isinstance(start, int) and isinstance(finish, int):
            if list_size:
                # generate list of random integer values
                return lambda: _random_int_list(
                    start, finish, list_size
                )
            else:
                # generate single random integer value
                return lambda: randint(start, finish)
        if isinstance(start, float) and isinstance(finish, float):
            # generate random float value
            round_digits = kwargs.pop('round_digits', 4)
            if list_size:
                return lambda: _random_float_list(
                    start, finish, list_size, round_digits
                )
            else:
                return lambda: round(
                    uniform(start, finish), round_digits
                )
        else:
            raise ValueError('Wrong parameters')

    if values and isinstance(values, (list, tuple, set)):
        # choose random value from collection
        return lambda: choice(values)


def generator_factory(start, step):
    """Factory of sequence generators."""
    def _gen():
        current_value = start
        while True:
            yield current_value
            current_value += step

    return _gen


def render_value(value):
    """Rendering of values of various types for VCF data.

    :param value: the value to be prepared for writing to the text file.
    """
    if isinstance(value, (tuple, list)):
        return ",".join([str(v) for v in value])
    else:
        return str(value)


class _BaseMetaField(object):

    """Base class for mandatory and INFO-fields ."""

    def __init__(self, choice_func=None, generator=None, default=None):
        self._generator = generator
        self._default = default
        self.set_choice_func(choice_func, generator, default)

    def set_choice_func(self, choice_func=None, generator=None, default=None):
        """Set or change choice function for a field."""
        if choice_func:
            self._choice_func = choice_func
        elif generator:
            self._generator = generator()
            if hasattr(self._generator, 'next'):
                self._choice_func = self._generator.next
            else:
                self._choice_func = self._generator.__next__
        else:
            self._choice_func = lambda: default

    @property
    def choice_value(self):
        """fill the value(s)."""
        return self._choice_func()


class MandatoryField(_BaseMetaField):

    """Metadata of one item from VCF mandatory fields, e.g. CHROM, ID, etc."""

    def __init__(self, choice_func=None, generator=None, default=None,
                 **params):

        self._field_params = MandatoryFields(**params)
        super(MandatoryField, self).__init__(choice_func, generator, default)


class MetaInfoItemField(_BaseMetaField):

    """Metadata of one item from INFO-section."""

    _render_format = {DESCRIPTION: '{0}="{1}"'}
    _default_render_format = '{0}={1}'

    def __init__(self, choice_func=None, generator=None, default=None,
                 **params):
        params[DESCRIPTION] = (
            params.get(DESCRIPTION, '') or
            INFO_DESCRIPTION.get(params[ID], DEFAULT_INFO_DESCRIPTION)
        )

        self._field_params = InfoItemFields(**params)
        self.ID = self._field_params.ID
        super(MetaInfoItemField, self).__init__(
            choice_func, generator, default
        )

    @property
    def rendered_info_items(self):
        result = []
        for key, value in zip(INFO_SECTION_KEYS, self._field_params):
            fmt_str = self._render_format.get(
                key, self._default_render_format
            )
            result.append(fmt_str.format(key, render_value(value)))

        result = ",".join(result)
        return "##INFO=<%s>" % result


class VCFData(object):

    """Generate VCF-data: vcf-file and the data as list of dicts."""

    def __init__(self, filename, lines=DEFAULT_VCF_CHUNK_SIZE,
                 fileformat=None):
        self._filename = filename
        self._fileformat = fileformat or DEFAULT_VCF_FILE_FORMAT
        self._mandatory_metadata = {}
        self._info_metadata = {}
        self._data = []
        self._chunk_size = lines

    def _info_field_metadata(self, info_field):
        if info_field.startswith(_INFO_PREFIX):
            info_field = info_field[len(_INFO_PREFIX):]

        return self._info_metadata.get(info_field)

    def __len__(self):
        return len(self._data)

    @property
    def filename(self):
        return self._filename

    @property
    def chunk_size(self):
        return self._chunk_size

    @property
    def info_fields(self):
        return self._info_metadata.keys()

    def define_info_field(self, choice_func=None, generator=None, default=None,
                          **kwargs):
        """Add info subfield with their metadata."""
        info_key = kwargs['ID']
        self._info_metadata[info_key] = MetaInfoItemField(
            choice_func, generator, default, **kwargs
        )

    def define_mandatory_field(self, field, choice_func=None, generator=None,
                               default=None, **kwargs):
        self._mandatory_metadata[field] = MandatoryField(
            choice_func=choice_func,
            generator=generator,
            default=default,
            **kwargs
        )

    def _render_header_line(self):
        header = list(MANDATORY_FIELDS) + [INFO]
        return "#" + "\t".join(header)

    def _render_info_section_header(self):
        result = []
        self._sorted_info_fields = list(self._info_metadata.keys())
        self._sorted_info_fields.sort()
        for field in self._sorted_info_fields:
            item = self._info_metadata[field]
            result.append(item.rendered_info_items)

        return result

    def _render_data_rows(self):
        result = []
        for source_row in self._data:
            result_row = []
            for field in MANDATORY_FIELDS:
                result_row.append(render_value(source_row[field]))
            info_data = []
            for info_field in self._sorted_info_fields:
                value = source_row[
                    _INFO_PREFIX + self._info_metadata[info_field].ID
                ]
                info_data.append('%s=%s' % (
                    self._info_metadata[info_field].ID, render_value(value)
                ))
            info_data = ";".join(info_data)

            result_row.append(info_data)
            result.append("\t".join(result_row))

        return result

    def make(self, lines=None):
        """Make data list and render data rows."""
        if not self._mandatory_metadata:
            raise ValueError('No enough mandatory fields')
        if not self._info_metadata:
            raise ValueError('No enough INFO fields')

        for field in MANDATORY_FIELDS:
            if field not in self._mandatory_metadata:
                raise ValueError('Expected mandatory field <%s>' % field)

        count = lines or self._chunk_size

        for item in range(count):
            data_row = {}

            ref_value = alt_value = None
            # because ALT is not REF even in the fake test file ;-)
            while ref_value == alt_value:
                ref_value = self._mandatory_metadata[REF].choice_value
                alt_value = self._mandatory_metadata[ALT].choice_value

            data_row[REF] = ref_value
            data_row[ALT] = alt_value

            for field in tuple(set(MANDATORY_FIELDS) - {REF, ALT}):
                value = self._mandatory_metadata[field].choice_value
                data_row[field] = value

            for info_field in self._info_metadata.values():
                value = info_field.choice_value
                data_row[_INFO_PREFIX + info_field.ID] = value

            self._data.append(data_row)

    def change_choice_func(self, field, choice_func=None,
                           generator=None, default=None):
        """change function for data generation in a field."""
        if field in MANDATORY_FIELDS:
            self._mandatory_metadata[field].set_choice_func(
                choice_func, generator, default
            )
        elif field in self._info_metadata.keys():
            self._info_metadata[field].set_choice_func(
                choice_func, generator, default
            )
        else:
            raise ValueError('Unknown field <%s>' % field)

    def write(self):
        """write the vcf-file."""
        result_strings = []
        # 1) write fileformat
        result_strings.append('##fileformat=%s' % self._fileformat)

        # 2) write fileDate
        result_strings.append(date.today().strftime('##fileDate=%Y%m%d'))

        # 3) write INFO-section
        result_strings.extend(self._render_info_section_header())

        # 4) write header of data block
        result_strings.append(self._render_header_line())

        # 5) write data block
        result_strings.extend(self._render_data_rows())

        # 6) write all data to file
        with open(self._filename, 'w') as f:
            f.write("\n".join(result_strings))
            f.write("\n")

    def remove(self):
        try:
            os.remove(self._filename)
        except OSError:
            pass
