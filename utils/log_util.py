import gzip

gz_file = '/Users/mason/Project/playground/ansys_shell/micen-nginx2-master.mic.com-en.access.log-2020.0228.1135.gz'


def get_gzip_content(file):
    with gzip.open(file, 'rb') as f:
        file_content = f.readlines()
        for line in file_content:
            yield line.decode(encoding='utf-8')

