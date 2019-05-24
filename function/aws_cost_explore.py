import boto3

class AWSCOSTEXPLORER(object):
    def __init__(self):
        self.explorer_client=boto3.client('ce')

    def get_cost_usage(self):
        response = self.explorer_client.get_cost_and_usage(
            TimePeriod={
                'Start': '2019-05-01',
                'End': '2019-05-02'
            },
            # Granularity='DAILY' | 'MONTHLY' | 'HOURLY',
            Granularity='DAILY',
            Filter={
                # 'Or': [
                #     {'... recursive ...'},
                # ],
                # 'And': [
                #     {'... recursive ...'},
                # ],
                # 'Not': {'... recursive ...'},
                # 'Dimensions': {
                #     'Key': 'AZ' | 'INSTANCE_TYPE' | 'LINKED_ACCOUNT' | 'OPERATION' | 'PURCHASE_TYPE' | 'REGION' | 'SERVICE' | 'USAGE_TYPE' | 'USAGE_TYPE_GROUP' | 'RECORD_TYPE' | 'OPERATING_SYSTEM' | 'TENANCY' | 'SCOPE' | 'PLATFORM' | 'SUBSCRIPTION_ID' | 'LEGAL_ENTITY_NAME' | 'DEPLOYMENT_OPTION' | 'DATABASE_ENGINE' | 'CACHE_ENGINE' | 'INSTANCE_TYPE_FAMILY' | 'BILLING_ENTITY' | 'RESERVATION_ID',
                #     'Values': [
                #         'string',
                #     ]
                # },
                'Tags': {
                    'Key': 'System',
                    'Values': [
                        'BPM',
                    ]
                }
            },
            # Metrics=[
            #     'string',
            # ],
            # GroupBy=[
            #     {
            #         'Type': 'DIMENSION' | 'TAG',
            #         'Key': 'string'
            #     },
            # ],
            # NextPageToken='string'
        )
        print(response)

if __name__ == '__main__':
    app=AWSCOSTEXPLORER()
    app.get_cost_usage()
