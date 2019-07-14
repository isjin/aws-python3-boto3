import boto3


class AWSECR(object):
    def __init__(self):
        self.ecr_client = boto3.client('ecr')

    def repository_create(self,repository_name):
        response = self.ecr_client.create_repository(
            repositoryName=repository_name,
            # tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ]
        )
        print(response)

    def repository_delete(self, repository_name):
        response = self.ecr_client.delete_repository(
            # registryId='string',
            repositoryName=repository_name,
            # force=True | False
        )
        print(response)

    def repository_describe(self, repository_name):
        response = self.ecr_client.describe_repositories(
            # registryId='string',
            repositoryNames=[
                repository_name,
            ],
            # nextToken='string',
            # maxResults=123
        )
        print(response)

    def repositories_describe(self):
        response = self.ecr_client.describe_repositories(
            # registryId='string',
            # repositoryNames=[
            #     repository_name,
            # ],
            # nextToken='string',
            # maxResults=123
        )
        return response['repositories']


if __name__ == '__main__':
    app = AWSECR()
    app.repository_delete('test')
