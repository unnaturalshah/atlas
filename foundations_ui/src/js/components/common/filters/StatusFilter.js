import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../../actions/CommonActions';

const statuses = [{ name: 'Completed' }, { name: 'Processing' }, { name: 'Error' }];
const isStatusCheckbox = true;

class StatusFilter extends Component {
  constructor(props) {
    super(props);
    this.changeLocalParams = this.changeLocalParams.bind(this);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.unsetClearFilters = this.unsetClearFilters.bind(this);
    this.state = {
      columns: statuses,
      changeHiddenParams: this.props.changeHiddenParams,
      changedParams: this.props.hiddenInputParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
      showAllFilters: false,
    };
  }


  componentWillReceiveProps(nextProps) {
    this.setState({ columns: nextProps.columns });
  }

  onApply() {
    const { changeHiddenParams, changedParams, toggleShowingFilter } = this.state;
    changeHiddenParams(changedParams);
    toggleShowingFilter();
  }

  onCancel() {
    const { toggleShowingFilter } = this.state;
    this.setState({ changedParams: [] });
    toggleShowingFilter();
  }

  onClearFilters() {
    const emptyArray = [];
    this.setState({ changedParams: emptyArray, showAllFilters: true });
  }

  unsetClearFilters() {
    this.setState({ showAllFilters: false });
  }

  changeLocalParams(colName) {
    const { changedParams } = this.state;
    const copyArray = CommonActions.getChangedCheckboxes(changedParams, colName);
    this.setState({ changedParams: copyArray });
  }

  render() {
    const { columns, showAllFilters } = this.state;
    const checkboxes = CommonActions.getCheckboxes(
      columns, this.changeLocalParams, showAllFilters, this.unsetClearFilters, isStatusCheckbox,
    );

    return (
      <div className="filter-container column-filter-container elevation-1 status-filter-container">
        <div className="column-filter-header">
          <button
            type="button"
            onClick={this.onClearFilters}
            className="b--mat b--affirmative text-upper float-right"
          >
          Clear Filters
          </button>
        </div>
        <div className="column-filter-list">
          {checkboxes}
        </div>
        <div className="column-filter-buttons">
          <button type="button" onClick={this.onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={this.onApply} className="b--mat b--affirmative text-upper">Apply</button>
        </div>
      </div>
    );
  }
}

StatusFilter.propTypes = {
  columns: PropTypes.array,
  changeHiddenParams: PropTypes.func,
  changedParams: PropTypes.array,
  toggleShowingFilter: PropTypes.func,
  hiddenInputParams: PropTypes.array,
  showAllFilters: PropTypes.bool,
};

StatusFilter.defaultProps = {
  columns: statuses,
  changeHiddenParams: () => {},
  changedParams: [],
  toggleShowingFilter: () => {},
  hiddenInputParams: [],
  showAllFilters: false,
};

export default StatusFilter;
