# FORK from https://github.com/wonderbeyond/dotbot-if/blob/main/if.py
import glob
import os
import subprocess

import dotbot
from dotbot.dispatcher import Dispatcher
from dotbot.util import module
from dotbot.plugins import Clean, Create, Link, Shell


class If(dotbot.Plugin):
    _directive = 'if'

    def can_handle(self, directive):
        return directive == self._directive

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError(f'Cannot handle this directive {directive}')

        if isinstance(data, list):
            return all(self._handle_single_if(d) for d in data)

        return self._handle_single_if(data)

    def _handle_single_if(self, data):
        cond = data.get('cond')

        if not cond:
            raise ValueError('Missing "cond" parameter for "if" directive')
        if not isinstance(cond, str):
            raise ValueError('"cond" parameter must be a string')

        ret = subprocess.run(['bash', '-c', cond])
        is_met = ret.returncode == 0

        if (is_met and 'met' not in data) or (not is_met and 'unmet' not in data):
            return True

        return self._run_internal(data['met'] if is_met else data['unmet'])

    # uncomment to enable plugins
    # def _load_plugins(self):
    #     plugin_paths = self._context.options().plugins
    #     plugins = []
    #     for dir in self._context.options().plugin_dirs:
    #         for path in glob.glob(os.path.join(dir, '*.py')):
    #             plugin_paths.append(path)
    #     for path in plugin_paths:
    #         abspath = os.path.abspath(path)
    #         plugins.extend(module.load(abspath))
    #     if not self._context.options().disable_built_in_plugins:
    #         plugins.extend([Clean, Create, Link, Shell])
    #     return plugins

    def _run_internal(self, data):
        dispatcher = Dispatcher(
            self._context.base_directory(),
            only=self._context.options().only,
            skip=self._context.options().skip,
            options=self._context.options(),
            # plugins=self._load_plugins(),
        )
        return dispatcher.dispatch(data)
