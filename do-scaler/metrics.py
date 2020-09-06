import requests
from prometheus_client.parser import text_string_to_metric_families # noqa


class Metrics:
    url_map = {
        'ip_address': lambda d: "http://{}".format(d.ip_address),
        'private_ip_address': lambda d: "http://{}".format(d.private_ip_address),
        'ip_v6_address': lambda d: "http://[{}]".format(d.ip_v6_address)
    }

    def __init__(self, config, droplet):
        self._set_attrs(config)
        self._metrics = self._get_metrics(droplet)

    def _set_attrs(self, config):
        for k, v in config.items():
            setattr(self, k, v)

    @staticmethod
    def _sample_to_dict(sample):
        return dict(zip(['name', 'labels', 'value', 'timestamp', 'exemplar'], sample))

    def _parse_metrics(self, metrics):
        parsed = {}
        for family in text_string_to_metric_families(metrics):
            parsed[family.name] = []
            for sample in family.samples:
                parsed[family.name].append(self._sample_to_dict(sample))
        return parsed

    def _build_url(self, droplet):
        return Metrics.url_map[self.address](droplet) + ":{}".format(self.port)

    def _get_metrics(self, droplet):
        r = requests.get(self._build_url(droplet))
        return self._parse_metrics(r.text)

    def sample_value(self, family, name):
        for sample in self._metrics[family]:
            if sample['name'] == name:
                return sample['value']
