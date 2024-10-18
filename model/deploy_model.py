import sagemaker
from sagemaker.tensorflow import TensorFlowModel

# Set up SageMaker session
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

# S3 URI of your uploaded model
model_data = 's3://your-bucket-name/models/lstm_autoencoder.tar.gz'

# Create a TensorFlow model
model = TensorFlowModel(
    model_data=model_data,
    role=role,
    framework_version='2.4.1',
    py_version='py37'
)

# Deploy the model
predictor = model.deploy(
    initial_instance_count=1,
    instance_type='ml.t2.medium',
    endpoint_name='lstm-autoencoder-endpoint'
)

print(f"Model deployed. Endpoint: {predictor.endpoint_name}")