# Copyright 2024 INRAE, French National Research Institute for Agriculture, Food and Environment
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
import typing
import os
import sys

from . import input_utils


@dataclass
class PlantModel:
    filename: str
    height: float
    filepath: str | None = None
    width: float = 0.0
    leaf_area: float = 0.0


@dataclass
class Plant:
    x: float = 0.0
    y: float = 0.0
    radius: float = 0.0
    height: float = 0.0


class PlantManager:
    def __init__(self):
        """
        Initializes the PlantManager and loads plant data from the default
        assets directory and the user-specific plants directory if it exists.
        """
        self.plant_groups = {}
        self.load_plants(os.path.abspath("assets/plants"))

        user_plants_dir = os.path.join(input_utils.user_data_dir(), "plants")
        if os.path.isdir(user_plants_dir):
            self.load_plants(user_plants_dir)

    def load_plants(self, dirname: str):
        """
        Loads plant data from the specified directory and updates the plant groups.

        Args:
            dirname (str): The directory name from which to load plant data.
        """
        if not os.access(dirname, os.R_OK):
            return

        for plant_dir in os.scandir(dirname):
            data = input_utils.load_config_file("description", plant_dir.path)
            if data is not None:
                self.update_groups(plant_dir, data)

    def update_groups(self, plant_dir: os.DirEntry, description: dict):
        """
        Updates the plant groups with the models defined in the given description.

        Args:
            plant_dir (os.DirEntry): The directory entry for the plant directory.
            description (dict): The plant description containing model data.
        """
        plant_type = plant_dir.name

        if "model_groups" in description:
            msg = "the description.yaml use the deprecated 'model_groups' syntax."
            msg += " Please, rewrite it using the new one."
            print(f"Warning: while loading plant model '{plant_type}': {msg}", file=sys.stderr)
            model_list = self.create_models_from_groups(plant_dir, description)

        elif "models" in description:
            model_list = self.create_models(plant_dir, description)

        else:
            raise RuntimeError(
                "Error: invalid description for plant model '{plant_type}': "
                + "the description.yaml file does not contain 'models' element."
            )

        self.plant_groups[plant_type] = model_list

    def create_models(self, plant_dir: os.DirEntry, description: dict) -> list[PlantModel]:
        """
        Creates a list of PlantModel instances based on the provided description.

        Parameters:
        - plant_dir (os.DirEntry): The plant directory containing model files.
        - description (dict): The dictionary corresponding to the description.yaml file.

        Returns:
        - list[PlantModel]: A list of initialized PlantModel instances.
        """
        model_list = []
        for model_data in description["models"]:
            model = PlantModel(
                filename=model_data["filename"],
                height=model_data.get("height"),
                width=model_data.get("width", 0.0),
                leaf_area=model_data.get("leaf_area", 0.0),
            )
            model.filepath = os.path.join(plant_dir.path, model.filename)
            model_list.append(model)
        return model_list

    def create_models_from_groups(
        self, plant_dir: os.DirEntry, description: dict
    ) -> list[PlantModel]:
        """
        Creates a list of PlantModel using the old syntax of the description.
        It expects 'model_groups' instead of the more recent 'models' syntax.

        Parameters:
        - plant_dir (os.DirEntry): The plant directory containing model files.
        - description (dict): The dictionary corresponding to the description.yaml file.

        Returns:
        - list[PlantModel]: A list of initialized PlantModel instances.
        """
        model_list = []
        for group in description["model_groups"].values():
            for model_data in group["models"]:
                model = PlantModel(
                    filename=model_data["filename"],
                    height=model_data.get("height"),
                    width=model_data.get("width", 0.0),
                    leaf_area=model_data.get("leaf_area", 0.0),
                )
                model.filepath = os.path.join(plant_dir.path, model.filename)
                model_list.append(model)
        return model_list

    def get_model_list_by_height(
        self, type: str, height: float, tolerance_coeff
    ) -> typing.List[PlantModel] | None:
        """
        Retrieves a list of plant models of a specific type within a height range
        defined by the given height and tolerance coefficient.

        Args:
            type (str): The type of plant to retrieve models for.
            height (float): The target height of the models.
            tolerance_coeff (float): The coefficient to determine the height range.

        Returns:
            List[PlantModel] | None: A list of matching plant models or None if none are found.
        """
        if type not in self.plant_groups:
            return None

        model_list = self.plant_groups[type]

        lower_bound = (1 - tolerance_coeff) * height
        higher_bound = (1 + tolerance_coeff) * height

        correct_models = [
            model
            for model in model_list
            if model.height >= lower_bound and model.height <= higher_bound
        ]
        return correct_models if correct_models else None
