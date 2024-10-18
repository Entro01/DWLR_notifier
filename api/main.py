from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import json
import numpy as np
import requests
from datetime import datetime

app = FastAPI()

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
sagemaker_runtime = boto3.client('sagemaker-runtime')

dwlr_info_table = dynamodb.Table('DWLRInfo')
model_info_table = dynamodb.Table('ModelInfo')

class WaterLevelData(BaseModel):
    dwlr_id: str
    timestamp: str
    water_level: float

@app.post("/process_data")
async def process_data(data: WaterLevelData):
    try:
        # Get model info
        model_info = model_info_table.get_item(Key={'dwlr_id': data.dwlr_id})
        if 'Item' not in model_info:
            raise HTTPException(status_code=404, detail="Model info not found")
        
        endpoint_name = model_info['Item']['sagemaker_endpoint']
        
        # Prepare input data (assuming the model expects a sequence of 10 values)
        input_data = np.array([data.water_level] * 10).reshape(1, 10, 1).tolist()
        
        # Get prediction from SageMaker endpoint
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=json.dumps(input_data)
        )
        
        result = json.loads(response['Body'].read().decode())
        
        # Check if it's an anomaly (you might need to adjust this logic)
        is_anomaly = result[0][0] > 0.1  # Assuming the model returns an anomaly score
        
        if is_anomaly:
            # Get DWLR info
            dwlr_info = dwlr_info_table.get_item(Key={'dwlr_id': data.dwlr_id})
            if 'Item' not in dwlr_info:
                raise HTTPException(status_code=404, detail="DWLR info not found")
            
            # Prepare alert data
            alert_data = {
                'dwlr_id': data.dwlr_id,
                'timestamp': data.timestamp,
                'water_level': data.water_level,
                'state': dwlr_info['Item']['STATE_UT'],
                'district': dwlr_info['Item']['DISTRICT'],
                'site_name': dwlr_info['Item']['SITE_NAME'],
                'well_type': dwlr_info['Item']['WELL_SITE_TYPE'],
                'reporting_officer': dwlr_info['Item']['REPORTING_OFFICER']
            }
            
            # Send alert to web portal
            web_portal_response = requests.post('https://your-web-portal.com/alert', json=alert_data)
            web_portal_response.raise_for_status()
        
        return {"message": "Data processed successfully", "is_anomaly": is_anomaly}
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to send alert to web portal: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)