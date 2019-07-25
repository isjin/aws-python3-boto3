import paramiko
import time


# option={
#     'host':'',
#     'port':'',
#     'username':'',
#     'pkey':'',
# }

class SSHTunnel(object):
    def __init__(self):
        pass

    @staticmethod
    def ssh_tunnel(options):
        hostname = options['host']
        port = options['port']
        username = options['username']
        pkey = options['pkey']
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hostname, port=port, username=username, key_filename=pkey)
        return client

    def ssh_channel(self, options, command):
        ssh = self.ssh_tunnel(options)
        channel = ssh.invoke_shell()
        channel.send(command + '\n')
        time.sleep(1)

    def __sftp_channel(self, options):
        return self.ssh_tunnel(options).open_sftp()

    def sftp_upload(self, options, local_file, remote_file):
        sftp = self.__sftp_channel(options)
        sftp.put(local_file, remote_file)

    def sftp_download(self, options, remote_file, local_file):
        sftp = self.__sftp_channel(options)
        sftp.get(remote_file, local_file)

    def chmod_file(self, options, exec_file, permission):
        command = 'sudo chmod %s %s' % (permission, exec_file)
        self.ssh_channel(options, command)

    def run_script(self, options, local_file, remote_file):
        self.sftp_upload(options, local_file, remote_file)
        self.chmod_file(options, remote_file, '755')
        command = 'nohup sudo /bin/bash %s&' % remote_file
        self.ssh_channel(options, command)
        self.del_file(options, remote_file)

    def del_file(self, options, remote_file):
        command = 'sudo rm -rf %s' % remote_file
        self.ssh_channel(options, command)
