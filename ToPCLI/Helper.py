import sys
import textwrap
import subprocess

class Table(object):
    def __init__(self, col_padding=2, min_col_width=12):
        self._header = None
        self._rows = []
        self._col_padding = col_padding
        self._min_col_width = min_col_width
        self._no_reduce = []

    def _find_columns_by_name(self, column_names):
        if type(column_names) is not list:
            column_names = [ column_names ]
        for name in column_names:
            if name in self._header:
                yield self._header.index(name)

    def header_is(self, header):
        self._header = [ str(i) for i in header ]
    def padding_is(self, col_padding):
        self._col_padding = col_padding
    def min_col_width_is(self, min_col_width):
        self._min_col_width = min_col_width
    def no_reduce(self, column_names):
        self._no_reduce = list(self._find_columns_by_name(column_names))

    def add_row(self, row):
        self._rows.append([ str(i) for i in row ])

    def sort(self, column_names):
        return sorted(self._rows,
            key=lambda row: tuple([row[i] for i in
                                   self._find_columns_by_name(column_names)]))

    def render(self):
        self._max_width = \
            int(subprocess.check_output(['stty', 'size']).decode().split()[1])
        output = sys.stdout
        width = []

        def find_width(row):
            for i in range(0, len(row)):
                while i >= len(width):
                    width.append(0)
                w = len(row[i])
                if w > width[i]:
                    width[i] = w

        def reduction_amount(col_width):
            col_width = col_width - self._min_col_width
            return col_width if col_width else self._min_col_width

        def print_row(row):
            lines = []
            for c in range(0, len(row)):
                wrapped = textwrap.wrap(row[c], width[c])

                for r in range(0, len(wrapped)):
                    while len(lines) <= r:
                        lines.append([])
                    while len(lines[r]) <= c:
                        lines[r].append("")
                    lines[r][c] = wrapped[r]
            for r in range(0, len(lines)):
                for c in range(0, len(lines[r])):
                    if c:
                        output.write(col_padding)
                    output.write("%-*s" % (width[c], lines[r][c]))
                output.write("\n")

        if self._header:
            find_width(self._header)
        for row in self._rows:
            find_width(row)

        columns = len(width)
        if not columns:
            # empty table
            return

        total_width = sum(width)
        total_width_limit = self._max_width - (columns - 1) * self._col_padding
        width_reduction = total_width - total_width_limit

        reductions = [ reduction_amount(col_width) for col_width in width ]
        total_reduction = sum(reductions)
        for i in range(0, columns):
            if i in self._no_reduce:
                continue
            if width_reduction <= 0:
                break
            reduction = width_reduction * reductions[i]
            if reduction:
                reduction = (reduction +
                             total_reduction - 1) / total_reduction
            if width[i] - reduction < self._min_col_width:
                reduction = width[i] - self._min_col_width
                if reduction < 0:
                    reduction = 0
            width[i] -= int(reduction)
            width_reduction -= reduction
            total_reduction -= reductions[i]

        col_padding = " " * self._col_padding

        if self._header:
            print_row(self._header)
            print_row([ '-' * col_width for col_width in width ])

        for row in self._rows:
            print_row(row)

        output.flush()
