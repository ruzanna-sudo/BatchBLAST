import os

BASE_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"

def load_config():
    if not os.path.exists('config'):
        with open('config', 'w+') as f:
            f.write('mL\n1000\nblastn\nnt\nbos taurus\nsus scrofa') # filter, output qty, program, database, non anomaly keyword, report species name
        return ["mL", 1000, "blastn", "nt", "sus scrofa", "Sample"]
    else:
        configs_ = []
        configs = []
        with open('config', 'r') as f:
            configs_ = f.readlines()
        for config in configs_:
            configs.append(config.replace('\n', ''))
        return configs[0], configs[1], configs[2], configs[3], configs[4], configs[5]



CONFIG = {
    'normal_sample_size': 5
}
