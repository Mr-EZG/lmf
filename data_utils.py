import os
import pandas as pd

def infer_csv_values(csv_df):
    columns = list(csv_df.columns)
    csv_dic = csv_df.to_dict('dict')
    class_dict = dict()
    for key in columns:
        if str(key) == 'file' or str(key) == 'files': 
            continue
        class_mappings = dict()
        i = 0
        for val in list(set(csv_dic.get(key, {}).values())):
            class_mappings[val] = i
            i += 1
        class_dict[key] = class_mappings
    return csv_dic, class_dict


def check_dirs(class_dict, base_dir):
    addresses = class_dict.get("address", {}).keys()
    for address in addresses:
        dir_path = os.path.join(base_dir, address)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

def copy_file():
    pass



if __name__ == '__main__':
    dir_of_data = "/Users/ethangarza/lmf"
    columns = ["name", "address", "top_y", "bottom_y", "top_y", "bottom_x", "label"]
    csv_df = pd.read_csv(val_labels_path)
    csv_dic, class_dict = infer_csv_values(csv_df)