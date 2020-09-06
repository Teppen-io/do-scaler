import json
import digitalocean # noqa
from os import path
from time import sleep


class Action():
    droplet_dir = path.join(path.abspath(path.dirname(__file__)), '../../droplets')

    def __init__(self, config):
        self._set_attrs(config)
        self._droplet_dir = getattr(self, 'droplet_dir', Action.droplet_dir)

    def _set_attrs(self, config):
        for k, v in config.items():
            setattr(self, k, v)

    def _build_droplet_config(self, config, num_droplets):
        config['token'] = self.do_token
        config['name'] = config['name'].format(num_droplets + 1)
        return config

    def _load_droplet_config(self):
        with open(self._droplet_dir + "/{}".format(self.droplet), 'r') as f:
            return json.load(f)

    def _get_droplet_config(self, num_droplets):
        config = self._load_droplet_config()
        return self._build_droplet_config(config, num_droplets)

    @staticmethod
    def _create_droplet(config):
        d = digitalocean.Droplet(**config)
        d.create()
        return d

    @staticmethod
    def _wait_status(droplet):
        while True:
            status = droplet.get_action(droplet.action_ids[0]).status
            if status == 'completed':
                break
            elif status == 'errored':
                raise Exception("Error creating droplet: {}".format(droplet.id))
            sleep(5)

    def run(self, initial_droplets, created_droplets, deleted_droplets):
        num_droplets = len(initial_droplets)

        if num_droplets < int(self.max):
            config = self._get_droplet_config(num_droplets)
            droplet = self._create_droplet(config)
            self._wait_status(droplet)
