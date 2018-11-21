import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';
import CommonActions from '../../js/actions/CommonActions';

configureTests();

const inputParams = [
  'myParam',
  'my2ndParam',
];
const emptyHeader = '';
const header = 'abc';
const emptyJob = {};
const job = {
  input_params: [
    {
      name: 'param1',
      value: {
        type: 'constant',
        value: '1',
      }
    },
    {
      name: 'param2',
      value: {
        type: 'constant',
        value: '3',
      }
    }
  ],
  output_metrics: {
    data_set_name: [
      'metric1',
      'metric2',
      'metric3',
    ],
  }
};
const cellWidths = [ 100, 200 ];
const jobs = [
  {
    job_id: 'job1',
    status: 'completed',
    input_params: [
      {
        name: 'param1',
      },
      {
        name: 'param2',
      }
    ]
  },
  {
    job_id: 'job2',
    status: 'running',
    input_params: [
      {
        name: 'param1',
      },
      {
        name: 'param2',
      }
    ]
  }
];
const functionStub = () => null;
const noError = false;
const error = true;
const hiddenParams = ['param2'];
const noMetric = false;
const metric = true;
const columns = ['param1', 'param2'];
const metricCols = ['metric1', 'metric2', 'metric3'];
const hidden = ['param2', 'metric3'];
const columnsToFormat = ['col1', 'col2', 'metric3'];
const emptyArray = [];
const changedParams = ['alreadyHere'];
const toAddParams = ['alreadyHere'];
const newParam = 'newParam';
const oldParam = 'alreadyHere';

it('getTableSectionHeaderDiv empty header', () => {
  const header = '';
  const className = CommonActions.getTableSectionHeaderDiv(header);
  expect(className).toBe('table-section-header');
});

it('getTableSectionHeaderArrow empty header', () => {
  const header = '';
  const className = CommonActions.getTableSectionHeaderArrow(header);
  expect(className).toBe('');
});

it('getTableSectionHeaderText empty header', () => {
  const header = '';
  const className = CommonActions.getTableSectionHeaderText(header);
  expect(className).toBe('blue-header-text text-white no-margin');
});

it('getTableSectionHeaderDiv with header', () => {
  const header = 'header';
  const className = CommonActions.getTableSectionHeaderDiv(header);
  expect(className).toBe('table-section-header blue-header');
});

it('getTableSectionHeaderArrow with header', () => {
  const header = 'header';
  const className = CommonActions.getTableSectionHeaderArrow(header);
  expect(className).toBe('blue-header-arrow border-input-metric-arrow');
});

it('getTableSectionHeaderText with header', () => {
  const header = 'header';
  const className = CommonActions.getTableSectionHeaderText(header);
  expect(className).toBe('blue-header-text text-white');
});

it('get InputMetricColumnHeaders', () => {
  const headers = CommonActions.getInputMetricColumnHeaders(inputParams, functionStub, hiddenParams);
  expect(headers.length).toBe(2);
});

it('isHeaderNotEmpty isFull', () => {
  const headers = CommonActions.isHeaderNotEmpty(header);
  expect(headers).toBe(true);
})

it('isHeaderNotEmpty isEmpty', () => {
  const headers = CommonActions.isHeaderNotEmpty(emptyHeader);
  expect(headers).toBe(false);
})

it('get InputMetricCells no metric, has jobs', () => {
  const cells = CommonActions.getInputMetricCells(job, cellWidths, error, noMetric, columns, hidden);
  expect(cells.length).toBe(2);
});

it('get InputMetricCells no metric, no job', () => {
  const cells = CommonActions.getInputMetricCells(emptyJob, cellWidths, error, noMetric, columns, hidden);
  expect(cells).toBe(null);
});

it('get InputMetricCells metric, has jobs', () => {
  const cells = CommonActions.getInputMetricCells(job, cellWidths, error, metric, metricCols, hidden);
  expect(cells.length).toBe(3);
});

it('get InputMetricCells metric, no job', () => {
  const cells = CommonActions.getInputMetricCells(emptyJob, cellWidths, error, metric, metricCols, hidden);
  expect(cells).toBe(null);
});

it('get InputMetricRows no jobs, ', () => {
  const rows = CommonActions.getInputMetricRows(emptyJob, cellWidths, noMetric, columns, hidden);
  expect(rows).toBe(null);
});

it('get InputMetricRows jobs', () => {
  const rows = CommonActions.getInputMetricRows(jobs, cellWidths, noMetric, columns, hidden);
  expect(rows.length).toBe(2);
  expect(rows[0]).not.toBe(null);
  expect(rows[1]).not.toBe(null);
});

it('get InputMetricCellPClass', () => {
  const metricClass = CommonActions.getInputMetricCellPClass(noError);
  expect(metricClass).toBe('font-bold');
});

it('get InputMetricCellPClass error', () => {
  const metricClass = CommonActions.getInputMetricCellPClass(error);
  expect(metricClass).toBe('font-bold error');
});

it('get InputMetricCellDivClass', () => {
  const metricClass = CommonActions.getInputMetricCellDivClass(noError);
  expect(metricClass).toBe('job-cell');
});

it('get InputMetricCellPDivlass error', () => {
  const metricClass = CommonActions.getInputMetricCellDivClass(error);
  expect(metricClass).toBe('job-cell error');
});

it('get InputParamHeaders', () => {
  const headers = CommonActions.getInputParamHeaders(inputParams, functionStub, hidden);
  expect(headers.length).toBe(2);
});

it('isError', () => {
  const isError = CommonActions.isError(jobs[0].status);
  expect(isError).toBe(false);
});

it('get InputCellsFromInputParams', () => {
  const cells = CommonActions.getInputCellsFromInputParams(job, cellWidths, noError, columns, noMetric, hidden);
  expect(cells.length).toBe(2);
  expect(cells[1]).toBe(null);
  expect(cells[0]).not.toBe(null);
});

it('get MetricCellsFromOutputMetrics', () => {
  const cells = CommonActions.getMetricCellsFromOutputMetrics(job, cellWidths, noError, metricCols, metric, hidden);
  expect(cells.length).toBe(3);
  expect(cells[0]).not.toBe(null);
  expect(cells[1]).not.toBe(null);
  expect(cells[2]).toBe(null);
});

it('formatColumns, no cols', () => {
  const formatedCols = CommonActions.formatColumns(emptyArray, hidden);
  expect(formatedCols).toEqual([]);
});

it('formatColumns, has cols', () => {
  const formatedCols = CommonActions.formatColumns(columnsToFormat, hidden);
  expect(formatedCols.length).toEqual(3);
  expect(formatedCols[1].hidden).toEqual(false);
  expect(formatedCols[2].hidden).toEqual(true);
});

it('get ChangedCheckboxes, old', () => {
  const changedArray = CommonActions.getChangedCheckboxes(changedParams, oldParam);
  expect(changedArray.length).toBe(0);
});

it('get ChangedCheckboxes, newParam', () => {
  const changedArray = CommonActions.getChangedCheckboxes(toAddParams, newParam);
  expect(changedArray.length).toBe(2);
  expect(changedArray[1]).toBe(newParam);
});