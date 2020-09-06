#!/usr/bin/env python3
import time
import sched
from os import path
from glob import glob
from configparser import ConfigParser, ExtendedInterpolation
from scaler import Scaler


class Scheduler:
    config_path = path.join(path.abspath(path.dirname(__file__)), '../do-scaler.cfg')
    confd_dir = path.join(path.abspath(path.dirname(__file__)), '../conf.d')

    def __init__(self, **kwargs):
        config = self._read_config(kwargs.get('config_path', Scheduler.config_path))
        self._set_attrs(config['scheduler'])
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._scalers = self._parse_scaler_configs(getattr(self, 'confd_dir', Scheduler.confd_dir))

    def _set_attrs(self, config):
        for k, v in config.items():
            setattr(self, k, v)

    def _read_config(self, location):
        config = ConfigParser(interpolation=ExtendedInterpolation())
        with open(path.expanduser(location)) as f:
            config.read_file(f)
        return config

    def _parse_scaler_configs(self, location):
        scalers = []
        for scaler_config in list(glob(path.abspath(location) + '/*.cfg')):
            parsed_config = self._read_config(scaler_config)
            scaler = Scaler(parsed_config)
            scalers.append(scaler)
        return scalers

    def _run_scalers(self):
        for scaler in self._scalers:
            scaler.run()

    def _run_forever(self):
        self._run_scalers()
        self._scheduler.enter(int(self.interval), 1, self._run_forever)

    def run(self):
        self._run_scalers()
        self._scheduler.enter(int(self.interval), 1, self._run_forever)
        self._scheduler.run()

    @property
    def config(self):
        return self._config

    @property
    def scalers(self):
        return self._scalers


def main():
    Scheduler().run()


if __name__ == "__main__":
    main()
