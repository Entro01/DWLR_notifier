import boto3

def create_dwlr_info_table(dynamodb):
    table = dynamodb.create_table(
        TableName='DWLRInfo',
        KeySchema=[
            {
                'AttributeName': 'dwlr_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'dwlr_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return table

def create_model_info_table(dynamodb):
    table = dynamodb.create_table(
        TableName='ModelInfo',
        KeySchema=[
            {
                'AttributeName': 'dwlr_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'dwlr_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return table

def main():
    dynamodb = boto3.resource('dynamodb')
    
    dwlr_info_table = create_dwlr_info_table(dynamodb)
    model_info_table = create_model_info_table(dynamodb)

    dwlr_info_table.meta.client.get_waiter('table_exists').wait(TableName='DWLRInfo')
    model_info_table.meta.client.get_waiter('table_exists').wait(TableName='ModelInfo')

    print("DynamoDB tables created successfully.")

    # Example of inserting data into DWLRInfo table
    dwlr_info_table.put_item(
        Item={
            'dwlr_id': 'DWLR001',
            'STATE_UT': 'Andhra Pradesh',
            'DISTRICT': 'Anantapur',
            'TEHSIL_BLOCK': 'Amarapuram',
            'VILLAGE_NAME': 'Palasamudram',
            'SITE_NAME': 'Palasamudram',
            'LATITUDE': '13.9605',
            'LONGITUDE': '77.6761',
            'WELL_SITE_TYPE': 'Dug Well',
            'REPORTING_OFFICER': 'John Doe'
        }
    )

    # Example of inserting data into ModelInfo table
    model_info_table.put_item(
        Item={
            'dwlr_id': 'DWLR001',
            'model_name': 'LSTM_Autoencoder_v1',
            'sagemaker_endpoint': 'lstm-autoencoder-endpoint-001',
            'last_trained': '2023-10-18',
            'performance_metric': '0.95'
        }
    )

if __name__ == "__main__":
    main()