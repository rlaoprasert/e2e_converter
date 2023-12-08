import os
import glob
import re
from typing import List

import oct_converter
from oct_converter.image_types.oct import OCTVolumeWithMetaData
from oct_converter import readers

def convert(path):
    e2e_files = get_e2e_files(path)
    for f in e2e_files:
        dir_path = os.path.dirname(f)
        file_name = os.path.basename(f)
        eye_flag = None
        if "_OD" in file_name:
            eye_flag = 'OD'
        elif "_OS" in file_name:
            eye_flag = 'OS'
        
        out_dir = os.path.join(dir_path, eye_flag)
        matches = re.search(f"_(\d+_{eye_flag})", file_name)
        filename_base = matches.groups()[0]
        print(filename_base)
        convert_e2e(f, out_dir, filename_base)

def get_e2e_files(path):
    p = os.path.join(path, '**', '*.e2e')
    print(f"Searching for *.e2e files in: {p}")
    e2e_files: List[str] = glob.glob(p, recursive=True)
    print(f"Num e2e files found: {len(e2e_files)}")
    return e2e_files


def create_directory():
    pass

def convert_e2e(path, output_dir, filename_base):
    print(f"Converting: {path} to {output_dir} ({filename_base})")
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    e2e = readers.E2E(path)
    oct_volume: List[OCTVolumeWithMetaData] = e2e.read_oct_volume()
    for i in range(len(oct_volume)):
        current_volume = oct_volume[i]
        vol_dir = os.path.join(output_dir, f"Volume{i}")
        if not os.path.isdir(vol_dir):
            os.mkdir(vol_dir)
        path = os.path.join(vol_dir, f"{filename_base}_vol{i}_.png")
        current_volume.save(path)



path = '/Users/rick/Documents/e2e'
convert(path)
