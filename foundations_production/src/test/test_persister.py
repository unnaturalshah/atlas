"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_production.persister import Persister

class TestPersister(Spec):
    
    archiver = let_mock()
    transformer = let_mock()

    @let
    def transformer_id(self):
        return '{}_{}'.format(self.faker.word(), self.faker.random_int())

    @let
    def transformer_artifact_name(self):
        return 'preprocessor/' + self.transformer_id

    @let
    def persister(self):
        return Persister(self.archiver)

    def test_save_transformer_saves_serialized_transformer_to_model_package(self):
        self.persister.save_user_defined_transformer(self.transformer_id, self.transformer)
        self.archiver.append_artifact.assert_called_with(self.transformer_artifact_name, self.transformer)

    def test_load_transformer_loads_serialized_transformer_from_model_package(self):
        self.archiver.fetch_artifact = ConditionalReturn()
        self.archiver.fetch_artifact.return_when(self.transformer, self.transformer_artifact_name)
        loaded_transformer = self.persister.load_user_defined_transformer(self.transformer_id)
        self.assertEqual(self.transformer, loaded_transformer)
