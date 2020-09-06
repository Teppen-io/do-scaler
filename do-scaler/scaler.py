import sys
import json
import digitalocean # noqa
from os import path
from metrics import Metrics
from policy import Policy
from importlib import import_module


class Scaler:
    policy_dir = path.join(path.abspath(path.dirname(__file__)), '../conf.d/policies')
    action_dir = path.join(path.abspath(path.dirname(__file__)), '../conf.d/actions')

    def __init__(self, config):
        self._config = config
        self._set_attrs(config['scaler'])
        self._manager = digitalocean.Manager(token=self.do_token)
        self._policies = self._create_policies()
        sys.path.append(getattr(self, 'action_dir', Scaler.action_dir))

    def _set_attrs(self, config):
        for k, v in config.items():
            setattr(self, k, v)

    def _load_policy_configs(self, policy_dir):
        policy_configs = []
        for file_name in self.policy_files.split():
            with open(policy_dir + "/{}".format(file_name), 'r') as f:
                policy_configs.append(json.load(f))
        return policy_configs

    def _create_policies(self):
        policies = []
        for config in self._load_policy_configs(getattr(self, 'policy_dir', Scaler.policy_dir)):
            policies.append(Policy(config))
        return policies

    def _import_actions(self, actions):
        modules = []
        for action in actions:
            mod = import_module(action)
            config = self._config[action]
            modules.append(mod.Action(config))
        return modules

    def _get_all_droplets(self):
        droplets = self._manager.get_all_droplets(tag_name=self.tag_name)
        if not droplets:
            raise Exception("No droplets found for tag_name: {}".format(self.tag_name))
        else:
            return droplets

    @staticmethod
    def _droplet_ids(droplets):
        return [d.id for d in droplets]

    def _deleted_droplets(self, droplets, new_droplets):
        deleted = set(self._droplet_ids(droplets)) - set(self._droplet_ids(new_droplets))
        return [d for d in droplets if d.id in deleted]

    def _created_droplets(self, droplets, new_droplets):
        created = set(self._droplet_ids(new_droplets)) - set(self._droplet_ids(droplets))
        return [d for d in new_droplets if d.id in created]

    def _droplet_state(self, droplets):
        curr_droplets = self._get_all_droplets()
        return (
            self._created_droplets(droplets, curr_droplets),
            self._deleted_droplets(droplets, curr_droplets)
        )

    def _run_actions(self, actions, droplets):
        created, deleted = [], []
        for action in actions:
            action.run(droplets, created, deleted)
            created, deleted = self._droplet_state(droplets)

    def _get_all_metrics(self, droplets):
        metrics = []
        for droplet in droplets:
            metrics.append(Metrics(self._config['scaler.metrics'], droplet))
        return metrics

    def run(self):
        for policy in self._policies:
            droplets = self._get_all_droplets()
            metrics = self._get_all_metrics(droplets)
            if policy.satisfied(metrics):
                actions = self._import_actions(policy.actions)
                self._run_actions(actions, droplets)
