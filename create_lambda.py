from function.aws_lambda import AWSLambda


class CreateLambda(object):
    def __init__(self):
        self.client = AWSLambda()

    def create_function(self):
        with open('lambda_function_snapshot_Brandgoods.zip', 'rb') as f:
            zipped_code = f.read()
        function_info = {
            'FunctionName': 'Brandgoods_snapshot_create',
            'Runtime': 'python3.6',
            'Role': 'arn:aws-cn:iam::168677335524:role/service-role/ec2_snapshot-role-ed4u0in8',
            'Handler': 'lambda_function_snapshot_Brandgoods.lambda_handler',
            'ZipFile': {'ZipFile': zipped_code},
        }
        self.client.lambda_function_create(function_info)


if __name__ == '__main__':
    app = CreateLambda()
    app.create_function()
