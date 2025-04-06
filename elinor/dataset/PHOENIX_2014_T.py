# TODO:
import os
from pathlib import Path
import pandas as pd
from typing import List, Optional
from elinor import count_files_by_end
import re
from PIL import Image

class BaseDatasetPhoenix2014T(object):
    """Phoenix-2014-T数据集基础类

    数据集结构大致如下：
    PHOENIX-2014-T-release-v3/
    └── PHOENIX-2014-T       <------- ROOT DIR
        ├── annotations
        │   └── manual
        ├── evaluation
        │   ├── sign-recognition
        │   └── sign-translation
        ├── features
        │   └── fullFrame-210x260px
        │       ├── dev
        │       ├── test
        │       └── train
        └── models
            └── languagemodels
    """
    def __init__(
            self, 
            root_dir="./PHOENIX-2014-T",
            split="dev" # train, test, dev
        ):
        self.root_dir=root_dir
        self.features_dir = os.path.join(self.root_dir, "features/fullFrame-210x260px", split)
        self.annotations_dir = os.path.join(self.root_dir, "annotations", "manual",)
        self.annoatation_df = pd.read_csv(
            os.path.join(self.annotations_dir, f"PHOENIX-2014-T.{split}.corpus.csv"),
            sep="|"
        ).rename(columns={"name": "dirname"})
        self._self_check_features_dir()
        self.feature_df = self._generate_feature_df()


    def _get_annotation_by_dirname(self, dirname):
        return self.annoatation_df[self.annoatation_df["dirname"] == dirname]
    

    def _self_check_features_png(self):
        dirs_to_check = [
            self.root_dir,
            self.features_dir,
            self.annotations_dir,
        ]
        for directory in dirs_to_check:
            if not os.path.isdir(directory):
                raise FileNotFoundError(f"Directory does not exist: {directory}")
        
        total_files = count_files_by_end(directory=self.features_dir, ends=".png")
        return total_files
    

    def _self_check_features_dir(self):
        subdirs = set()
        for root, dirs, files in os.walk(self.features_dir):
            for d in dirs:
                subdirs.add(d)
        # Check if the subdirectories match the names in the annotation DataFrame
        assert subdirs == set(self.annoatation_df.dirname.values), f"Subdirectories in {self.features_dir} do not match annotation names."
        return subdirs


    def _generate_feature_df(self):
        metadata_list = []
        metadata = {
            "dirname": None,
            "frame": None,
            "image": None,
        }
        pattern = r'(\d+)'
        
        for dirname in self.annoatation_df.dirname:
            dir_path = os.path.join(self.features_dir, dirname)
            files = sorted([f for f in os.listdir(dir_path) if f.endswith('.png')])
            for file in files:
                # Extract the frame number from the filename
                frame_number = int(re.search(pattern, file).group(1))
                metadata["dirname"] = dirname
                metadata["frame"] = frame_number
                metadata["image"] = file
                metadata_list.append(metadata.copy())
        # Create a DataFrame from the metadata list
        metadata_df = pd.DataFrame(metadata_list)

        return metadata_df

    def get_all_features_path_by_dirname(self, dirname):
        """
        Get all features by name
        Args:
            name: The name of the feature
        Returns:
            A DataFrame containing all features with the specified name
        """
        data = self.feature_df[self.feature_df["dirname"] == dirname].sort_values(by="frame").image
        return [os.path.join(self.features_dir, dirname, file) for file in data]

    def get_all_features_generator_by_dirname(self, dirname):
        """
        Get all features by name
        Args:
            name: The name of the feature
        Returns:
            A DataFrame containing all features with the specified name
        """
        data = self.get_all_features_path_by_dirname(dirname)
        for i, path in enumerate(data):
            yield Image.open(path)

if __name__ == '__main__':
    dataset = BaseDatasetPhoenix2014T()
