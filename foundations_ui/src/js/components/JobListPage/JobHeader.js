import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ShowMoreFilters from '../common/filters/ShowMoreFilters';
import CommonActions from '../../actions/CommonActions';
import JobListActions from '../../actions/JobListActions';

const borderSize = 3; // 1px per side + space between bubbles

class JobHeader extends Component {
  constructor(props) {
    super(props);
    this.toggleFilters = this.toggleFilters.bind(this);
    this.clickRemoveFilter = this.clickRemoveFilter.bind(this);
    this.showHideBubbles = this.showHideBubbles.bind(this);
    this.addIfNotHidden = this.addIfNotHidden.bind(this);
    this.removeFromHidden = this.removeFromHidden.bind(this);
    this.getHiddenWidth = this.getHiddenWidth.bind(this);
    this.addToBubbleRefs = this.addToBubbleRefs.bind(this);
    this.removeBubbleFromRef = this.removeBubbleFromRef.bind(this);
    this.modifyBubble = this.modifyBubble.bind(this);
    this.refsInFilters = this.refsInFilters.bind(this);
    this.getCurHiddenBubbles = this.getCurHiddenBubbles.bind(this);
    this.removeHiddenButtonCallback = this.removeHiddenButtonCallback.bind(this);
    this.cancelJobs = this.cancelJobs.bind(this);
    this.onDeletedJobs = props.onDeletedJobs.bind(this);
    this.state = {
      project: this.props.project,
      jobs: this.props.jobs,
      filters: this.props.filters,
      bubbleRefs: [],
      isShowingMoreFilters: false,
      clearFilters: this.props.clearFilters,
      removeFilter: this.props.removeFilter,
      hiddenBubbles: [],
    };
  }

  onDeletedJobs() {
    console.log('jobs deleted');
  }

  async componentWillReceiveProps(nextProps) {
    this.setState({ filters: nextProps.filters, project: nextProps.project });

    const { hiddenBubbles } = this.state;
    const newRefs = this.refsInFilters(nextProps.filters);

    const curWidth = 0;
    let curHiddenBubbles = CommonActions.deepCopyArray(hiddenBubbles);
    curHiddenBubbles = this.getCurHiddenBubbles(newRefs, curHiddenBubbles);
    newRefs.sort((a, b) => { return a.length - b.length; });
  }

  refsInFilters(filters) {
    return filters.map((filter) => {
      return `${filter.column}-${filter.value}`;
    });
  }

  getCurHiddenBubbles(newRefs, hiddenBubbles) {
    return hiddenBubbles.filter((bubble) => {
      return newRefs.indexOf(bubble) >= 0;
    });
  }

  showHideBubbles(id, curWidth, clientWidth, hiddenBubbles) {
    let bubbleWidth = curWidth;
    let curHiddenBubbles = CommonActions.deepCopyArray(hiddenBubbles);
    if (id !== null) {
      const bubble = document.getElementById(id);
      if (bubble !== null) {
        const modifyBubbleResults = this.modifyBubble(
          curHiddenBubbles, id, bubble, bubbleWidth, clientWidth,
        );
        bubbleWidth = modifyBubbleResults.width;
        curHiddenBubbles = modifyBubbleResults.hiddenBubbles;
      }
    }
    return { width: bubbleWidth, hiddenBubbles: curHiddenBubbles };
  }

  modifyBubble(hiddenBubbles, id, bubble, curWidth, clientWidth) {
    let bubbleWidth = curWidth;
    let curHiddenBubbles = CommonActions.deepCopyArray(hiddenBubbles);
    const hiddenWidth = this.getHiddenWidth(hiddenBubbles, id);
    const curBubbleWidth = CommonActions.addBorderToElementWidth(bubble, borderSize, hiddenWidth);
    bubbleWidth += curBubbleWidth;
    if (CommonActions.elementsWidthLargerThanParent(bubbleWidth, clientWidth)) {
      if (bubble && bubble.className && !bubble.className.includes(' hidden')) {
        bubble.className += ' hidden';
        curHiddenBubbles = this.addIfNotHidden(curHiddenBubbles, id, curBubbleWidth);
      }
    } else if (bubble && bubble.className && bubble.className.includes(' hidden')) {
      bubble.className = bubble.className.replace(' hidden', '');
      curHiddenBubbles = this.removeFromHidden(curHiddenBubbles, id);
    }
    return { width: bubbleWidth, hiddenBubbles: curHiddenBubbles };
  }

  addIfNotHidden(array, id, width) {
    const newHidden = this.removeFromHidden(array, id);
    newHidden.push({ id, width });
    return newHidden;
  }

  removeFromHidden(array, id) {
    let newHidden = CommonActions.deepCopyArray(array);
    newHidden = newHidden.filter(
      (filter) => {
        return (filter.id && filter.id !== id) || (!filter.id && filter !== id);
      },
    );
    return newHidden;
  }

  getHiddenWidth(array, id) {
    let newHidden = CommonActions.deepCopyArray(array);
    newHidden = newHidden.filter(
      (filter) => {
        return (filter.id === id);
      },
    );
    if (newHidden[0]) {
      return newHidden[0].width;
    }
    return null;
  }

  toggleFilters() {
    const { isShowingMoreFilters, hiddenBubbles } = this.state;
    if (hiddenBubbles.length > 0) {
      this.setState({ isShowingMoreFilters: !isShowingMoreFilters });
    }
  }

  async clickRemoveFilter(filter) {
    const { removeFilter, bubbleRefs } = this.state;
    const id = filter.column.concat('-').concat(filter.value);
    const currentBubbleRefs = this.removeBubbleFromRef(bubbleRefs, id);
    await removeFilter(filter);
    await this.setState({ bubbleRefs: currentBubbleRefs });
  }

  addToBubbleRefs(key) {
    const { bubbleRefs } = this.state;
    if (!bubbleRefs.includes(key)) {
      bubbleRefs.push(key);
    }
  }

  removeBubbleFromRef(bubbleRefs, id) {
    return bubbleRefs.filter((bubble) => {
      if (bubble !== id) {
        return true;
      }
    });
  }

  removeHiddenButtonCallback(filterToRemove) {
    this.clickRemoveFilter(filterToRemove);
  }

  async cancelJobs() {
    if (window.confirm('Are you sure you want to cancel all running and queued jobs?')) {
      const jobIds = this.props.jobs
        .filter(job => job.status === 'running' || job.status === 'queued')
        .map(job => job.job_id);
      return JobListActions.deleteAllJobs(jobIds, this.onDeletedJobs);
    }
  }

  render() {
    const {
      project, jobs, filters, isShowingMoreFilters, clearFilters, hiddenBubbles,
    } = this.state;

    const filterBubbles = [];
    filters.forEach((filter) => {
      const key = filter.column.concat('-').concat(filter.value);
      filterBubbles.push(
        <div ref={() => { this.addToBubbleRefs(key); }} id={key} key={key} className="bubble inline-block">
          <p className="font-bold">
            {filter.column}:<span> {filter.value}</span>
          </p>
          <button onClick={() => { this.clickRemoveFilter(filter); }} type="button" className="close-button" />
        </div>,
      );
    });

    let moreBubbles = null;
    if (hiddenBubbles.length > 0) {
      moreBubbles = (
        <div className="bubble more-bubble">
          <p className="font-bold text-blue text-upper">
          + {hiddenBubbles.length} More
          </p>
        </div>
      );
    }

    let moreFilters = null;
    let filterButtonText = 'View Filters';
    if (isShowingMoreFilters) {
      moreFilters = (
        <ShowMoreFilters
          hiddenBubbles={hiddenBubbles}
          removeFilterCallback={this.removeHiddenButtonCallback}
        />
      );
      filterButtonText = 'Hide Filters';
    }
    let viewFilterClass = 'b--mat b--affirmative text-upper';
    if (hiddenBubbles.length === 0) {
      viewFilterClass += ' b--disabled';
      moreFilters = null;
    }
    let clearFiltersClass = 'b--mat b--affirmative text-upper';
    if (filters.length === 0) {
      clearFiltersClass += ' b--disabled';
    }

    return (
      <div className="job-header-container">
        <div className="job-header-container-left">

          <div className="job-summary-info-container">
            <h2 className="font-bold project-list-name">{project.name}</h2>
            <h3>Jobs List</h3>
            <ul>
              <li>
                <p className="font-bold">Project owner: </p>
                <p>Trial<span>{project.owner}</span></p>
              </li>
              <li>
                <p className="font-bold">Created at: </p>
                <p>Trial</p>
              </li>
            </ul>
          </div>
          {moreFilters}
        </div>
        <div className="deleteJobWrapper">
          <button
            className="deleteButton"
            type="button"
            onClick={this.cancelJobs}
            onKeyDown={() => {}}
          >
            Delete Queued and Running Jobs
          </button>
        </div>
      </div>
    );
  }
}

JobHeader.propTypes = {
  numProjects: PropTypes.number,
  project: PropTypes.object,
  filters: PropTypes.array,
  bubbleRefs: PropTypes.array,
  isShowingMoreFilters: PropTypes.bool,
  clearFilters: PropTypes.func,
  removeFilter: PropTypes.func,
  hiddenBubbles: PropTypes.array,
  jobs: PropTypes.array,
  onDeletedJobs: PropTypes,
};

JobHeader.defaultProps = {
  numProjects: 0,
  project: { owner: 'null', created_at: 'null', name: 'null' },
  filters: [],
  bubbleRefs: [],
  isShowingMoreFilters: false,
  clearFilters: () => {},
  removeFilter: () => {},
  hiddenBubbles: [],
  jobs: [],
  onDeletedJobs: () => { window.location.reload(); },
};

export default JobHeader;