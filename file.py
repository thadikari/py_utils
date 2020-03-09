import csv
import os


def resolve_data_dir(proj_name):
    SCRATCH = os.environ.get('SCRATCH', None)
    if not SCRATCH: SCRATCH = os.path.join(os.path.expanduser('~'), 'SCRATCH')
    return os.path.join(SCRATCH, proj_name)

def resolve_data_dir_os(proj_name, extra=[]):
    if os.name == 'nt': # if windows
        curr_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(curr_path, '..', '..', 'data', *extra)
    else:
        return resolve_data_dir(proj_name)


class CSVFile:
    def __init__(self, file_name, work_dir, header):
        path = os.path.join(work_dir, file_name)
        self.fp = open(path, 'w', newline='')
        self.csv = csv.writer(self.fp, delimiter=',')
        self.csv.writerow(header)

    def writerow(self, line, flush=False):
        self.csv.writerow(line)
        if flush: self.flush()

    def flush(self): self.fp.flush()

    def __del__(self):
        self.fp.flush()
        self.fp.close()