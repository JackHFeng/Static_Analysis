import os
import shutil

# 'E:/Desktop/solc/current'
# f'E:/Desktop/solc/{version}'


def set_solc_version(src_dir, dst_dir, version):
    print(f'Changing solc version to {version}')
    remove_all_files(dst_dir)
    copy_all_files(src_dir, dst_dir, version)


def remove_all_files(dst_dir):
    folder = dst_dir
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def copy_all_files(src_dir, dst_dir, version):
    src = os.path.join(src_dir, version)
    for filename in os.listdir(src):
        file_path = os.path.join(src, filename)
        shutil.copy(file_path, dst_dir)

