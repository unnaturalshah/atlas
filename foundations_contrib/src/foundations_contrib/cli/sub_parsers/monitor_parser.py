"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class MonitorParser(object):
    
    def __init__(self, commandline):
        self._cli = commandline

    def add_sub_parser(self):
        from argparse import REMAINDER
        
        monitor_help = 'Provides operations for managing monitors in Orbit'
        monitor_parser = self._cli.add_sub_parser('monitor', help=monitor_help)
        monitor_sub_parser = monitor_parser.add_subparsers()

        pause_parser = monitor_sub_parser.add_parser('pause')
        pause_parser.add_argument('project_name', type=str)
        pause_parser.add_argument('monitor_name', type=str)
        pause_parser.add_argument('--env', type=str, required=False, help='Specifies the scheduler environment')
        pause_parser.set_defaults(function=self._pause_monitor)

        start_parser = monitor_sub_parser.add_parser('start')
        start_parser.add_argument('--name', type=str, help='Name of monitor to delete')
        start_parser.add_argument('--project_name', type=str, help='Project that the monitor will be created in')
        start_parser.add_argument('--env', type=str, required=False, help='Specifies the scheduler environment')
        start_parser.add_argument('job_directory', type=str, help='Directory from which to schedule the monitor')
        start_parser.add_argument('command', type=str, nargs=REMAINDER, help='Monitor script to schedule')
        start_parser.set_defaults(function=self._start_monitor)

        delete_parser = monitor_sub_parser.add_parser('delete')
        delete_parser.add_argument('project_name', metavar='project_name', help='Project that the monitor will be deleted from')
        delete_parser.add_argument('name', type=str, metavar='name', help='Name of monitor to delete')
        delete_parser.add_argument('--env', type=str, required=False, help='Specifies the scheduler environment')
        delete_parser.set_defaults(function=self._delete_monitor)

        resume_parser = monitor_sub_parser.add_parser('resume')
        resume_parser.add_argument('project_name', type=str)
        resume_parser.add_argument('monitor_name', type=str)
        resume_parser.add_argument('--env', type=str, required=False, help='Specifies the scheduler environment')
        resume_parser.set_defaults(function=self._resume_monitor)


    def _delete_monitor(self):
        from foundations_contrib.cli.orbit_monitor_package_server import delete

        env = self._cli.arguments().env if self._cli.arguments().env is not None else 'scheduler'
        project_name = self._cli.arguments().project_name
        monitor_name = self._cli.arguments().name

        delete(project_name, monitor_name, env)

    def _start_monitor(self):
        from foundations_contrib.cli.orbit_monitor_package_server import start

        arguments = self._cli.arguments()
        job_directory = arguments.job_directory
        command = arguments.command
        project_name = arguments.project_name
        name = arguments.name
        env = self._cli.arguments().env if self._cli.arguments().env is not None else 'scheduler'
        
        start(job_directory, command, project_name, name, env)

    def _pause_monitor(self):
        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import  CronJobSchedulerError
        from foundations_contrib.cli.orbit_monitor_package_server import pause
        
        monitor_name = self._cli.arguments().monitor_name
        project_name = self._cli.arguments().project_name
        env = self._cli.arguments().env if self._cli.arguments().env is not None else 'scheduler'

        try:
            pause(project_name, monitor_name, env)
        except CronJobSchedulerError as ce:
            import sys
            sys.exit(str(ce))

    def _resume_monitor(self):
        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobSchedulerError
        from foundations_contrib.cli.orbit_monitor_package_server import resume
        
        monitor_name = self._cli.arguments().monitor_name
        project_name = self._cli.arguments().project_name
        env = self._cli.arguments().env if self._cli.arguments().env is not None else 'scheduler'

        try:
            resume(project_name, monitor_name, env)
        except CronJobSchedulerError as ce:
            import sys
            sys.exit(str(ce))
