from .crops import crops_node_group
from .gaussian_random import gaussian_random_node_group

def create_all_node_group():
    crops_node_group()
    gaussian_random_node_group()
