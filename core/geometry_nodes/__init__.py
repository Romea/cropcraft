from .crops import crops_node_group
from .scattering import scattering_node_group
from .stones_scattering import stones_scattering_node_group

def create_all_node_group():
    crops_node_group()
    scattering_node_group()
    stones_scattering_node_group()
