import React from 'react';
import ReactDOM from 'react-dom';
import ProjectPage from '../../js/components/ProjectPage/ProjectPage';
import { shallow, mount } from 'enzyme';
import { MemoryRouter } from 'react-router-dom';
import configureTests from '../setupTests';
import ProjectActions from '../../js/actions/ProjectActions';

configureTests();

it('Shallow Renders ProjectPage', () => {
  const wrapper = shallow(<ProjectPage/>);
  expect(wrapper).toMatchSnapshot();
});

it('Calls Get All Projects', async () => {
  <MemoryRouter>
    const wrapper = mount(<ProjectPage/>); 
    const preState = wrapper.state();
    await wrapper.instance().getAllProjects();
    const postState = wrapper.state();
    expect(preState.isLoaded === false);
    expect(postState.isLoaded === true);
  </MemoryRouter>
});

// Assumes your API has projects
it('Has at least One Project', async () => {
  <MemoryRouter>
    const wrapper = mount(<ProjectPage/>); 
    const preState = wrapper.state();
    await wrapper.instance().getAllProjects();
    const postState = wrapper.state();
    expect(preState.projects.length === 0);
    expect(postState.projects.length > 0);
  </MemoryRouter>
});

it('Sets QueryStatus Based on getProjects Response', async () => {
  <MemoryRouter>
    ProjectActions.getProjects = jest.fn();
    ProjectActions.getProjects.status.mockReturnValue({404});
    const wrapper = mount(<ProjectPage/>); 
    const preState = wrapper.state();
    await wrapper.instance().getAllProjects();
    expect(preState.queryStatus).toEqual(200);
    expect(wrapper.state.queryStatus).toEqual(404);
  </MemoryRouter>
});
