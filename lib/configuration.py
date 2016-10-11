#!/usr/bin/env python
"""
Configuration handling for tower companion
"""
from __future__ import print_function, absolute_import
import os
import requests.packages.urllib3 as urllib3
from .utils import BadKarma

# in python 3, ConfigParser has been renamed configparser
try:
    from ConfigParser import ConfigParser, NoOptionError, DuplicateSectionError
except ImportError:
    # python 3
    from configparser import ConfigParser, NoOptionError, DuplicateSectionError


class Config(object):
    def __init__(self, config_file):
        configparser = ConfigParser()
        if config_file:
            configparser.read(config_file)
        self.config_file = config_file
        self.configparser = configparser
        self._add_general_section()
        # now the configuration is initialized with the content of the
        # configuration file. Next step is to read the environment and check
        # if there are any values provided by th
        self._update_from_env('TC_USERNAME', 'username')
        self._update_from_env('TC_PASSWORD', 'password')
        self._update_from_env('TC_HOST', 'host')
        self._update_from_env('TC_VERIFY_SSL', 'verify_ssl')
        self._update_from_env('TC_RECKLESS_MODE', 'reckless_mode')

        # decide whatever we need to suppress some bad output because we did not
        # have decent SSL certifcates
        self._reckless_mode()

    def get(self, option):
        """
        nice and cozy method to interact to read values from your configuration.
        Returns the value of 'option' from the 'general' section.
        If option is not found, it raises a BadKarma exception.
        Params:
            option (str): option you want to read from in memory configuration

        Returns:
            (str): value of the option from the 'general' section

        Raises:
            BadKarma
        """
        config = self.configparser
        try:
            return config.get('general', option)
        except NoOptionError as error:
            raise BadKarma(error)

    def has_option(self, option):
        """
        Checks whatever config has 'option'
        """
        config = self.configparser
        return config.has_option('general', option)

    def update(self, option, value):
        """
        Updates a configuration value
        section is hardcoded to 'general'
        Params:
            option (str): option you want to value from in memory configuration

            value (str): value you want to set
        """
        config = self.configparser
        config.set(section='general', option=option, value=value)

    def write(self):
        """
        Saves current configuration to config_file
        """
        config = self.configparser
        config.write(self.config_file)

    def _add_general_section(self):
        """
        In case your configuration file is so bad that you don't have a
        'general' section
        """
        config = self.configparser
        try:
            config.add_section('general')
        except DuplicateSectionError:
            # yeah nothing to do, the section already exist
            pass

    def _update_from_env(self, env_variable, option):
        """
        Gets configuration from the current environment, values set in the
        environment take precedence on the one configured in the standard
        configuration file.

        Params:
            env_variable (str): name of the environmental variable to use

            option (str): name of configuration
        """
        value = os.environ.get(env_variable)
        if value:
            self.update(option=option, value=value)

    def _reckless_mode(self):
        """
        Live fast, die young, get hacked and cry.
        If you're here, you have bad SSL certficates
        urllib3, used by requests, clobbers the output with a lot of SSL warnings
        the following lines, just disables the warning messages.

        Enable this only if you're a bad person.
        """
        config = self.configparser
        try:
            if config.getboolean('general', 'reckless_mode'):
                # look reckless mode!
                urllib3.disable_warnings()
        except NoOptionError:
            # reckless mode is not even configured, it's an exception but it is
            # the happiest path!
            return
