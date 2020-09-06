
class Action():
    def __init__(self, config):
        self._set_attrs(config)

    def _set_attrs(self, config):
        for k, v in config.items():
            setattr(self, k, v)

    @staticmethod
    def _destroy_droplet(droplet):
        if not droplet.destroy():
            raise Exception("Error destroying droplet: {}".format(droplet.name))

    def run(self, initial_droplets, created_droplets, deleted_droplets):
        if len(initial_droplets) > int(self.min):
            self._destroy_droplet(initial_droplets[0])
