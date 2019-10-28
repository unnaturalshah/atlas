"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy
import pandas
from foundations_spec import *
from foundations_orbit.contract_validators.special_values_checker import SpecialValuesChecker


class TestSpecialValuesChecker(Spec):

    @let
    def contract_options(self):
        from foundations_orbit.data_contract_options import DataContractOptions
        return DataContractOptions(
            max_bins=50,
            check_row_count=True,
            special_values=[numpy.nan],
            check_distribution=True,
            check_special_values=True,
            distribution=self.distribution_options
        )
    @let
    def distribution_options(self):
        return {
            'distance_metric': 'l_infinity',
            'default_threshold': 0.1,
            'cols_to_include': None,
            'cols_to_ignore': None,
            'custom_thresholds': {},
            'custom_methods': {}
        }

    @let_now
    def empty_dataframe(self):
        import pandas
        return pandas.DataFrame()


    @let_now
    def one_column_dataframe(self):
        return pandas.DataFrame(columns=[self.column_name], data=[4], dtype=numpy.int8)

    @let
    def bin_stats_one_column(self):
        return {
            self.column_name: [{
                'value': 4,
                'percentage': 1.0,
                'upper_edge': None
            }]
        }
    
    @let_now
    def two_column_dataframe(self):
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[5,6],[10,32]], dtype=numpy.int8)

    @let
    def bin_stats_two_column_no_special_value(self):
        return {
            self.column_name: [{
                'percentage': 1.0,
                'upper_edge': 10
            }, {'percentage': 0.0, 'upper_edge': numpy.inf}],
            self.column_name_2: [{
                'percentage': 1.0,
                'upper_edge': 32
            }, {'percentage': 0.0, 'upper_edge': numpy.inf}]
        }

    @let
    def bin_stats_two_columns_with_special_values(self):
        return {
            self.column_name: [{
                'percentage': 1.0,
                'upper_edge': None
            }, {
                'value': numpy.nan,
                'percentage': 0.0
            }],
            self.column_name_2: [{
                'value': numpy.nan,
                'percentage': 0.0
            }, {
                'value': 1,
                'percentage': 1.0,
                'upper_edge': None
            }]
        }

    @let
    def bin_stats(self):
        return {
            self.column_name: [{
                'percentage': 1.0,
                'upper_edge': None
            }],
            self.column_name_2: [{
                'value': numpy.nan,
                'percentage': 0.0
            }, {
                'value': 1,
                'percentage': 1.0,
                'upper_edge': None
            }]
        }

    @let
    def bin_stats_one_column_no_special_value(self):
        return {
            self.column_name: [{
                'value': 1,
                'percentage': 1.0,
                'upper_edge': None
            }]
        }

    @let
    def column_name(self):
        return self.faker.word()

    @let
    def column_name_2(self):
        return self._generate_distinct([self.column_name], self.faker.word)

    @let_now
    def two_column_dataframe_no_rows(self):
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2])

    @let
    def reference_column_types_int(self):
        return {self.column_name: 'int', self.column_name_2: 'int'}

    def _generate_distinct(self, reference_values, generating_callback):
        candidate_value = generating_callback()
        return candidate_value if candidate_value not in reference_values else self._generate_distinct(reference_values, generating_callback)
    
    def test_schema_checker_can_accept_configurations(self):
        checker = SpecialValuesChecker(self.contract_options, None, None, {})
        self.assertIsNotNone(getattr(checker, "configure", None))
        
    def test_schema_checker_can_accept_exclusions(self):
        checker = SpecialValuesChecker(self.contract_options, None, None, {})
        self.assertIsNotNone(getattr(checker, "exclude", None))

    def test_special_values_check_for_mulitple_column_df_against_itself_returns_all_passed_using_not_previously_defined_special_value(self):
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats
        data = {
            self.column_name: [5, 10, 15, -1],
            self.column_name_2: [6, 32, 40, -1]
        }

        dataframe = pandas.DataFrame(data)
        special_values = [-1]
        self.contract_options.special_values = special_values

        bin_stats = {
            self.column_name: create_bin_stats(special_values, 10, pandas.Series(data[self.column_name])),
            self.column_name_2: create_bin_stats(special_values, 10, pandas.Series(data[self.column_name_2]))
        }

        expected_check_results = {
            self.column_name:{
                -1: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            }, 
            self.column_name_2:{
                -1: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25, 
                    'passed': True
                }
            }
        }

        checker = SpecialValuesChecker(self.contract_options, bin_stats, [self.column_name, self.column_name_2], self.reference_column_types_int, dataframe)
        checker.configure(attributes=[self.column_name, self.column_name_2], thresholds={ -1: 0.1 })
        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)


    def _create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(self, special_character):
        data = {
            self.column_name: [5, 10, 15, special_character],
            self.column_name_2: [6, 32, 40, special_character]
        }

        dataframe = pandas.DataFrame(data)
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats

        special_values = [special_character]

        bin_stats = {
            self.column_name: create_bin_stats(special_values, 10, pandas.Series(data[self.column_name])),
            self.column_name_2: create_bin_stats(special_values, 10, pandas.Series(data[self.column_name_2]))
        }
        return SpecialValuesChecker(self.contract_options, bin_stats, [self.column_name, self.column_name_2], {self.column_name: str(pandas.Series(data[self.column_name]).dtype),
         self.column_name_2: str(pandas.Series(data[self.column_name_2]).dtype)},dataframe), dataframe
    
    def test_special_values_checker_for_datetime_input_returns_expected_result(self):
        data = {
            self.column_name: [5, 10, 15, numpy.nan],
            self.column_name_2: [6, 32, 40, numpy.nan]
        }

        dataframe = pandas.DataFrame(data)
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats

        special_values = [numpy.nan]

        bin_stats = {
            self.column_name: create_bin_stats(special_values, 10, pandas.Series(data[self.column_name])),
            self.column_name_2: create_bin_stats(special_values, 10, pandas.Series(data[self.column_name_2]))
        }

        checker = SpecialValuesChecker(self.contract_options, bin_stats, [self.column_name, self.column_name_2], {self.column_name: str(pandas.Series(data[self.column_name]).dtype),
         self.column_name_2: str(pandas.Series(data[self.column_name_2]).dtype)},dataframe)

        expected_check_results = {
            self.column_name:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            },
            self.column_name_2:{
                numpy.nan: {
                    'percentage_diff': 0.25,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.50,
                    'passed': False
                }
            }
        }

        checker.configure(attributes=[self.column_name, self.column_name_2], thresholds={numpy.nan: 0.1})
        dataframe_to_validate = dataframe.copy()
        dataframe_to_validate.iloc[0,1] = numpy.nan
        results = checker.validate(dataframe_to_validate)
        self.assertEqual(expected_check_results, results)

    def test_special_values_check_for_mulitple_column_df_against_itself_including_nans_returns_all_passed(self):
        expected_check_results = {
            self.column_name:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            },
            self.column_name_2:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25, 
                    'passed': True
                }
            }
        }

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.configure(attributes=[self.column_name, self.column_name_2], thresholds={numpy.nan: 0.1})
        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)

    def test_special_values_check_for_mulitple_column_df_against_itself_including_nans_returns_all_passed_for_configured_column(self):
        expected_check_results = {
            self.column_name:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            }
        }

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name], thresholds={numpy.nan: 0.1})

        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)

    def test_special_values_check_for_mulitple_column_df_against_itself_including_nans_returns_all_passed_excluding_column(self):
        expected_check_results = {
            self.column_name_2:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25, 
                    'passed': True
                }
            }
        }

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.configure(attributes=[self.column_name, self.column_name_2], thresholds={numpy.nan: 0.1})

        checker.exclude(attributes=[self.column_name])
        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)
    
    def test_special_values_checker_allows_exclude_all(self):
        expected_check_results = {}

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.exclude(attributes='all')
        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)

    def test_special_values_check_configure_multiple_times_appends_to_previous_configurations(self):
        expected_check_results = {
            self.column_name:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            },
            self.column_name_2:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            }
        }

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name], thresholds={numpy.nan: 0.1})
        checker.configure(attributes=[self.column_name_2], thresholds={numpy.nan: 0.1})
        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)

    def test_special_values_check_requires_attributes_as_a_parameter(self):
        checker, _ = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        try:
            checker.configure()
            self.fail('Failed to throw appropriate error message for missing attribute')
        except ValueError as ve:
            self.assertTrue('attribute is required' in str(ve).lower())

    def test_special_values_check_requires_threshold_as_a_parameter(self):
        checker, _ = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        try:
            checker.configure(attributes=[])
            self.fail('Failed to throw appropriate error message for missing attribute')
        except ValueError as ve:
            self.assertTrue('threshold is required' in str(ve).lower())

    def test_special_values_check_requires_threshold_as_a_parameter(self):
        checker, _ = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        try:
            checker.configure(attributes=[], thresholds=[])
            self.fail('Failed to throw appropriate error message for incorrectly specified threshold')
        except ValueError as ve:
            self.assertTrue('invalid threshold' in str(ve).lower())

    def test_special_values_check_configure_uses_values_in_thresholds_to_determine_if_passed(self):
        expected_check_results = {
            self.column_name:{
                numpy.nan: {
                    'percentage_diff': 0.25,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.5,
                    'passed': False
                }
            },
            self.column_name_2:{
                numpy.nan: {
                    'percentage_diff': 0.25,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.5,
                    'passed': True
                }
            }
        }

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name], thresholds={ numpy.nan: 0.1 })
        checker.configure(attributes=[self.column_name_2], thresholds={ numpy.nan: 0.5 })
        
        dataframe_to_validate = dataframe.copy()
        dataframe_to_validate.iloc[-2,:2] = numpy.nan

        results = checker.validate(dataframe_to_validate)
        self.assertEqual(expected_check_results, results)

    def test_special_values_check_configure_applies_values_in_thresholds_to_all_specified_columns_to_determine_if_passed(self):
        expected_check_results = {
            self.column_name:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            },
            self.column_name_2:{
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
            }
        }

        checker, dataframe = self._create_special_values_checker_and_dataframe_with_two_columns_with_special_characters(numpy.nan)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name, self.column_name_2], thresholds={numpy.nan: 0.1})
        results = checker.validate(dataframe)
        self.assertEqual(expected_check_results, results)

    def test_single_column_with_two_special_characters_produce_two_special_value_results(self):
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats
        special_values = [numpy.nan]
        data = {
            self.column_name: [5, 10, 15, 7, 7, 6, 8, numpy.nan]
        }

        dataframe = pandas.DataFrame(data)
        bin_stats = {
            self.column_name: create_bin_stats(special_values, 10, pandas.Series(data[self.column_name]))
        }
        checker = SpecialValuesChecker(self.contract_options, bin_stats, [self.column_name, self.column_name_2], {self.column_name: 'float'} ,dataframe)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name], thresholds={numpy.nan: 0.1, -1: 0.1})

        # modify the dataframe for there to be a difference between the bin stats generation and current state
        dataframe_to_be_validated = dataframe.copy()
        dataframe_to_be_validated.iloc[:2] = numpy.nan
        dataframe_to_be_validated.iloc[-2:] = -1

        expected_check_results = {
            self.column_name: {
                numpy.nan: {
                    'percentage_diff': 0.125,
                    'ref_percentage': 0.125,
                    'current_percentage': 0.25,
                    'passed': False
                },
                -1: {
                    'percentage_diff': 0.25,
                    'ref_percentage': 0.0,
                    'current_percentage': 0.25,
                    'passed': False
                }
            }
        }
        results = checker.validate(dataframe_to_be_validated)
        self.assertEqual(expected_check_results, results)

    def test_special_values_checker_configure_raises_value_error_when_unsupported_columns_used(self):
        reference_column_types = {self.column_name: 'str', self.column_name_2: 'object'}
        checker = SpecialValuesChecker(self.contract_options, self.bin_stats, [self.column_name, self.column_name_2], reference_column_types=reference_column_types)

        checker.configure(attributes=[self.column_name], thresholds={numpy.nan: 0.1})

        expected_error_dictionary = {
            self.column_name_2: 'object'
        }

        with self.assertRaises(ValueError) as e:
            checker.configure(attributes=[self.column_name_2], thresholds={numpy.nan: 0.1})

        self.assertEqual(f'The following columns have invalid types: {expected_error_dictionary}', e.exception.args[0])
    