from function.ssh_tunnel import SSHTunnel
from multiprocessing import Pool

hosts = [
    {
        'host': '52.83.254.152',
        'port': '22',
        'username': 'ec2-user',
        'pkey': 'key/devopschaindemo.pem'
    },
]
local_file = 'scripts/cloudwatch_memory_disk.sh'
remote_file = '/tmp/cloudwatch_memory_disk.sh'


class InitialCLoudWatch(object):
    def __init__(self):
        self.ssh_tunnel = SSHTunnel()

    # def run(self, option, file_local, file_remote):
    #     self.ssh_tunnel.run_script(option, file_local, file_remote)

    def main(self):
        p = Pool()
        for host in hosts:
            p.apply_async(self.ssh_tunnel.run_script,(host, local_file, remote_file))
            # self.ssh_tunnel.run_script(host, local_file, remote_file)
        p.close()
        p.join()


if __name__ == '__main__':
    app = InitialCLoudWatch()
    app.main()
