import os
from omegaconf import OmegaConf


class CTransformerConfig():
    def __init__(self):
        self.curdir = os.getcwd()
        self.conf = OmegaConf.load(os.path.join(
            self.curdir, 'Config', 'CTransformersBaseConfig.json'))
        self.top_k = self.conf.top_k
        self.top_q = self.conf.top_p
        self.temperature = self.conf.temperature
        self.last_n_tokens = self.conf.last_n_tokens
        self.max_new_tokens = self.conf.max_new_tokens
        self.gpu_layers = self.conf.gpu_layers

    def get_config(self):
        top_k = self.top_k
        top_q = self.top_q
        temperature = self.temperature
        last_n_tokens = self.last_n_tokens
        max_new_tokens = self.max_new_tokens
        gpu_layers = self.gpu_layers
        return top_k, top_q, temperature, last_n_tokens, max_new_tokens, gpu_layers
