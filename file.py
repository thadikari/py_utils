from itertools import zip_longest
import csv
import os


def resolve_data_dir(proj_name):
    scratch = os.path.join(os.path.expanduser('~'), 'scratch')
    return os.path.join(scratch, proj_name)

def resolve_data_dir_os(proj_name, extra=[]):
    if os.name == 'nt': # if windows
        curr_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(curr_path, '..', '..', 'data', *extra)
    else:
        return resolve_data_dir(proj_name)


class CSVFile:
    def __init__(self, file_name, work_dir=None, header=None, mode='w'):
        path = file_name if work_dir is None else os.path.join(work_dir, file_name)
        self.fp = open(path, mode, newline='')
        self.csv = csv.writer(self.fp, delimiter=',')
        if header is not None: self.csv.writerow(header)
        self.header = header

    def writerow(self, line, flush=False):
        self.csv.writerow(line)
        if flush: self.flush()

    def flush(self): self.fp.flush()

    def __del__(self):
        self.fp.flush()
        self.fp.close()


def filter_directories(_a, data_dir, sort_by_default=True):
    dirs = next(os.walk(data_dir))[1]
    kw_filter = lambda nl_,f_,kwl: [n_ for n_ in nl_ if f_(kw in n_ for kw in kwl)]
    if _a.and_kw: dirs = kw_filter(dirs, all, _a.and_kw)
    if _a.or_kw: dirs = kw_filter(dirs, any, _a.or_kw)

    ord = _a.order_dir
    if not dirs:
        print(f'No matching directories found in {data_dir}.')
        return dirs
    else:
        if ord:
            ord = [oo for oo,_ in zip_longest(ord, dirs, fillvalue=-1)]
            strings = [f'[{order:g}] {dir}' for order,dir in zip(ord,dirs)]
        else: strings = dirs
        print('Collected directories:', *strings, sep='\n')

    if ord: dirs = [dir for _,dir in sorted(zip(ord, dirs))]
    elif sort_by_default: dirs.sort()
    return dirs

def bind_dir_filter_args(parser):
    parser.add_argument('--and_kw', help='directory name AND filter: allows only if all present', default=[], type=str, nargs='*')
    parser.add_argument('--or_kw', help='directory name OR filter: allows if any is present', default=[], type=str, nargs='*')
    parser.add_argument('--order_dir', help='re-order dir list, biggest at the front', type=float, nargs='+')
