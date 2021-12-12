import sys

ref_dir_dict = {
    "hgdp": "/home/shussain/popviz/genomic_data/flipped",
    "1kgp": "/home/geb/Documents/bioinformatics/1000G_2504/"
}

try:
    print(ref_dir_dict[sys.argv[1]])
except KeyError:
    raise Exception(f"accepted reference names {list(ref_dir_dict.keys())}")