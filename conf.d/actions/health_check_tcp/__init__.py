import socket
from time import sleep


class Action():
    def __init__(self, config):
        self._set_attrs(config)

    def _set_attrs(self, config):
        for k, v in config.items():
            setattr(self, k, v)

    def _tcp_connect(self, address, port):
        for i in range(0, int(self.max_tries)):
            try:
                socket.create_connection(
                    (address, port),
                    timeout=int(self.timeout)
                )
            except socket.error:
                sleep(int(self.interval))
            else:
                return True

    def run(self, initial_droplets, created_droplets, deleted_droplets):
        for droplet in created_droplets:
            address = getattr(droplet, self.address)
            for port in self.ports.split():
                if not self._tcp_connect(address, port):
                    raise Exception("Could not connect to {}:{}".format(address, port))
