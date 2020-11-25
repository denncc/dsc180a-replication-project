import os
import json
config_path = "./config/config.json"

# retrive the data according to config/config
def data_retrieve():
    data_dir = config["data"][0]
    datasets = os.listdir(data_dir)
    datasets.sort()
    reference = datasets[-3:]
    datasets = datasets[:-3]
    result = []
    for i in range(0, len(datasets), 2):
        result.append([os.path.join(data_dir, datasets[i]), os.path.join(data_dir, datasets[i + 1])])
    for i in range(len(reference)):
        reference[i] = os.path.join(data_dir, reference[i])
    return result, reference


if __name__ == "__main__":
    # get the config file
    with open(config_path) as f:
        config = json.load(f)
    datas, reference = data_retrieve()
    print(datas[0], reference)