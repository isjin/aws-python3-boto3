from function.aws_lambda import AWSLambda


class CreateLambda(object):
    def __init__(self):
        self.client = AWSLambda()
        self.zip_path='lamdba/cloudwatch_metric_put/test.zip'

    def create_function(self):
        with open(self.zip_path, 'rb') as f:
            zipped_code = f.read()
        function_info = {
            'FunctionName': 'test',
            'Runtime': 'python3.6',
            'Role': 'arn:aws-cn:iam::646976741397:role/lambda_cloudwatch_metric_ec2',
            'Handler': 'test.lambda_handler',
            'ZipFile': {'ZipFile': zipped_code},
        }
        info=self.client.lambda_function_create(function_info)
        print(info)


if __name__ == '__main__':
    app = CreateLambda()
    app.create_function()
