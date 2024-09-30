# DWLR_notifier
SIH 2024 submission

Abstract

The Central Ground Water Board (CGWB) is implementing an extensive network of Digital Water Level Recorders (DWLRs) across India, aiming to monitor groundwater levels more effectively. With plans to install 14,000 DWLRs by 2026, each recording data at 6-hour intervals, the volume of data generated presents both opportunities and challenges in accurately detecting anomalies. To address these challenges, we propose a web portal served by a robust infrastructure designed to analyze high-frequency water level measurements, identify anomalies such as missing data and low battery levels, and alert appropriate authorities for prompt intervention.

At the core of our solution is the use of LSTM autoencoders for anomaly detection. LSTM (Long Short-Term Memory) networks are well-suited for handling sequential data, allowing the model to learn temporal dependencies inherent in the groundwater level data. This capability is crucial for detecting deviations from expected patterns, especially in a dynamic environment where various external factors influence groundwater levels. Our approach emphasizes the importance of training separate models for different geographical regions, as the hydrogeological characteristics and environmental conditions of DWLRs can vary significantly. This tailored modeling strategy enhances the accuracy of anomaly detection, ensuring that each model is finely tuned to the specific conditions of its corresponding DWLRs.

Data availability is pivotal to the efficacy of our models. As we gather more contextual data—such as the effects of low battery levels on DWLR readings—we can refine our models to make more accurate predictions regarding the causes of anomalies. In cases where certain data does not yet exist, we propose conducting experiments to collect relevant information or leveraging additional metadata from DWLRs, such as battery percentages. This continuous data collection and incorporation will further bolster the accuracy and reliability of the anomaly detection system.

The architecture of our system is built upon a robust AWS ecosystem, utilizing services such as Amazon S3 for model storage, Amazon Elastic Container Registry (ECR) for managing Docker containers, and AWS SageMaker for deploying inference endpoints. When new data arrives via API Gateway and AWS SQS, a Lambda function is triggered to route the data to the appropriate SageMaker endpoint based on the DWLR ID. The resulting inference outputs are stored in AWS Redshift, providing historical data tracking and facilitating the continuous training of models with newly acquired data.

Through this comprehensive approach, we aim to create an intelligent, scalable, and responsive system for monitoring groundwater levels across India. By effectively detecting anomalies and alerting the relevant authorities through a dedicated web portal, our solution not only enhances groundwater management but also contributes to the sustainable use of this vital resource. As we move forward, the adaptability of our system allows for future upgrades, such as integrating AWS Kinesis for real-time data streaming, ensuring that it remains capable of meeting the evolving needs of groundwater monitoring.

Idea Title: AnomalyWatch: Real TimeAnomaly Detection & Alerting Platform

Idea Description

The Central Ground Water Board (CGWB) is currently in the process of installing 14,000 Digital Water Level Recorders (DWLRs) across India to monitor groundwater levels as part of a larger water management initiative. These DWLRs will record water level data at 6-hour intervals, producing a substantial volume of data from all over the country. By 2026, the DWLR network will generate more than 20 million data points annually, creating a significant challenge in managing, analyzing, and identifying any anomalies, such as missing data or abnormal water levels. Identifying these anomalies quickly is crucial to ensure appropriate action is taken, especially if any DWLRs malfunction, record unusual water level patterns, or have battery failures.

Problem Overview:
The primary challenge is not only the large volume of data but also the complexity that comes with managing DWLRs across different geographic and environmental conditions. Each region might have varying groundwater dynamics based on its location, climate, and groundwater depth, which means that anomaly detection needs to be tailored accordingly. Given the scale and importance of this data, the solution needs to handle large-scale data efficiently while providing real-time insights to identify anomalies and alert the relevant officers in charge.

Proposed Solution:

The proposed solution involves a robust infrastructure built on AWS services that can manage periodic data from the DWLRs, apply machine learning for anomaly detection, and raise real-time alerts through a developed web portal to notify the appropriate authorities.

1) We are using API Gateway, Amazon SQS, and AWS Lambda for the data ingestion pipeline. API Gateway serves as the entry point, receiving data from the DWLRs every 6 hours and passing it to the system. Amazon SQS is used to temporarily queue the data, ensuring that even if there’s a large influx of requests from the 14,000 DWLRs, none of the data is lost, and it can be processed asynchronously by Lambda functions. The reason for using SQS is to decouple the data ingestion process from the processing, which provides flexibility and prevents overloading the system when multiple requests arrive simultaneously. This queue-based approach ensures that all data is handled efficiently and prevents bottlenecks, particularly during peak times when data is sent from all DWLRs at once.

2) Once the data enters SQS, it triggers AWS Lambda functions for processing. Each Lambda function processes a batch of data points by calling the respective machine learning model associated with the DWLR. These models are not pre-trained but are instead specifically trained by us using historical data collected from DWLRs installed so far. The data from each DWLR is used to train LSTM Autoencoder models for Anomaly Detection in AWS SageMaker. We aim to train different the LSTM Autoencoder model on different datasets made by using historical data such that we have different models for a pool of DWLRs.

The key reason we cannot rely on a single LSTM autoencoder model for all DWLRs is the significant variability in environmental conditions, groundwater behavior, and other region-specific factors across India. Each DWLR is located in a unique geographical area, which introduces a variety of challenges in terms of detecting anomalies with a one-size-fits-all model. Different Water Table Depths, Seasonal Variations, Climate and Weather Patterns, Water Usage and Human Activity, Local Environmental Factors all come into play. 

Given these variations, it is critical to have multiple LSTM autoencoder models that are specifically trained for groups of DWLRs that share similar characteristics. By clustering DWLRs based on location, depth, climate, and other environmental factors, we can fine-tune models that are sensitive to the local behaviors of groundwater levels. This approach allows the system to better distinguish between normal fluctuations and true anomalies, improving the accuracy of the detection process while minimizing false alarms and missed detections.

3) The inference results generated by the models are stored in AWS Redshift, creating a comprehensive historical database of all DWLR data points and their anomaly classifications. This data allows for deeper analysis and re-training over time, helping to track the performance of individual wells and detect long-term trends. 

4) When an anomaly is detected, the system generates an alert for the concerned officer responsible for that particular DWLR. This alert, along with the associated details such as the location of the well and the nature of the anomaly, is displayed on a web portal specifically developed for the reporting officers. These officers can access the portal to see detailed logs and take appropriate action in response to the anomaly. The web portal also allows for easy tracking of the status of each DWLR and provides real-time updates, ensuring that any potential issues are addressed promptly.

While the current setup relies on periodic data collection using SQS and Lambda, the system is designed to scale in the future. Should the CGWB require continuous data streams instead of periodic batch submissions, the system can be upgraded to AWS Kinesis, which would allow for real-time data ingestion and anomaly detection. Kinesis would enable continuous monitoring of groundwater levels, providing immediate insights as soon as the data is collected, and further improving the responsiveness of the system.

This solution not only addresses the immediate challenges of anomaly detection but also ensures that the system is scalable, flexible, and capable of handling the future growth of the DWLR network. Through the combination of AWS services, machine learning models, and a user-friendly web portal, the solution provides an efficient and reliable way to manage the large-scale groundwater monitoring project.

Indepth Discussion:

LSTM AutoEncoders for Anomaly Detection

We are using LSTM autoencoders for anomaly detection in this project because of their ability to handle sequential data, which is a critical characteristic of the time series data collected from the Digital Water Level Recorders (DWLRs). The key reason for choosing this type of model lies in the nature of the data and the problem itself—groundwater level measurements are taken periodically, and the data exhibits temporal dependencies, meaning that past measurements influence future values. LSTM (Long Short-Term Memory) networks are specifically designed to capture these temporal relationships, making them ideal for detecting anomalies in time series data.

Overview of LSTM Autoencoders

An LSTM autoencoder is a type of neural network that is composed of two parts: the encoder and the decoder.

- Encoder: The encoder LSTM processes the input sequence (e.g., a series of groundwater level measurements) and compresses it into a fixed-length latent representation, which is a condensed version of the data that captures its most important features. This latent space represents the underlying structure of the time series data and is crucial for understanding its normal behavior.

- Decoder: The decoder LSTM takes this compressed representation and attempts to reconstruct the original input sequence. The goal during training is to minimize the difference (error) between the original data and the reconstructed data.

In a normal situation, when the system is working correctly, the autoencoder can reconstruct the input sequence with low error because it has learned the patterns of normal behavior. However, when anomalous data (such as a sudden drop in groundwater levels or missing data) is fed into the model, the reconstruction error increases because the autoencoder has not seen these unusual patterns during training.

Why Autoencoders for Anomaly Detection?

1) Unsupervised Learning: One of the most important advantages of LSTM autoencoders is that they can be trained in an unsupervised manner. This means that we do not need labeled data to train the model. In the case of DWLRs, labeled anomaly data (i.e., data that has been pre-classified as normal or abnormal) is often unavailable or difficult to collect. By training the LSTM autoencoder only on normal data (historical data where no anomalies were reported), the model learns the normal patterns, and any deviation from these patterns is flagged as an anomaly.

2) Reconstruction Error for Anomaly Detection: The key to anomaly detection with autoencoders is the reconstruction error. Since the model is trained to recreate normal data, when an anomalous event occurs (such as a sudden spike or drop in groundwater level), the model will not be able to accurately reconstruct the input. This leads to a high reconstruction error, which is used as a signal to flag the data as anomalous. In our case, the reconstruction error is used to classify whether the water level data from a DWLR is normal or whether there’s an issue that needs attention.

3) Adapting to New Data: LSTM autoencoders are flexible and can be continuously retrained as new data becomes available. As more DWLRs are deployed and more data is collected, we can retrain or fine-tune the models to improve their performance over time, ensuring that they stay accurate as conditions change. This adaptability is important in a dynamic environment like groundwater monitoring, where seasonal changes and long-term trends can gradually shift the baseline behavior.

How the models are stored for Inference

The models used for anomaly detection in the DWLR system are stored and deployed using a combination of Amazon S3, Amazon Elastic Container Registry (ECR), and AWS SageMaker endpoints. This setup allows for seamless inference whenever new data is received from the DWLRs.

1) Model Storage in S3: The trained LSTM autoencoder models, once finalized, are stored in Amazon S3. S3 serves as a secure and scalable storage solution, ensuring that models are readily available for deployment or future updates. The model files are organized by their corresponding DWLR regions or groups, allowing for easy access and retrieval.

2) Model Deployment with ECR and SageMaker: For inference, the models are containerized using Docker and stored in Amazon Elastic Container Registry (ECR). ECR acts as a repository for these Docker images, ensuring that they can be deployed on-demand without manual intervention. Each model is tied to a specific DWLR or group of DWLRs, and the appropriate container is invoked whenever a request is made. AWS SageMaker endpoints are created for each model, enabling scalable and low-latency inference. These endpoints serve as an interface between the incoming data and the deployed models, handling the computation required to detect anomalies.

3) Lambda Function Inference: When new data is ingested from the DWLRs (via API Gateway and SQS), a Lambda function is triggered. This function retrieves the DWLR ID, identifies the corresponding model based on the stored information, and sends the collected data to the appropriate SageMaker endpoint for inference. The Lambda function is lightweight and event-driven, ensuring that the inference process is efficient and cost-effective. Once the inference is complete, the results (anomaly classification) are sent back and stored in AWS Redshift for historical tracking.

By leveraging this combination of S3, ECR, and SageMaker, the system is designed to be highly modular and scalable, allowing easy access to models and smooth integration with the rest of the data pipeline. This setup ensures that each DWLR’s unique model can be quickly accessed and used for inference, making the entire anomaly detection process both robust and efficient.

About Data Availability

Data availability plays a crucial role in improving the accuracy and reliability of the anomaly detection models. As we collect more data from the Digital Water Level Recorders (DWLRs), the system becomes better equipped to make accurate predictions about potential anomalies. One important aspect to consider is the availability of data that reflects the various external factors affecting DWLR readings, such as battery levels, environmental conditions, and mechanical faults.

For instance, if we have data on the effects of low battery levels on the accuracy of DWLR readings, we can incorporate this information into the LSTM autoencoder model. This would allow the model to distinguish between anomalies caused by environmental factors (like sudden changes in water levels) and those caused by a malfunctioning DWLR due to low battery power. If this type of data is available, the model can make a more informed prediction about the root cause of an anomaly, enabling appropriate actions to be taken more swiftly. For example, if the model detects an anomaly and identifies that the DWLR is operating on low battery, it can prioritize sending an alert to replace the battery before more serious issues arise.

However, in cases where this type of data does not yet exist, we can conduct experiments to gather information on how low battery levels or other factors impact DWLR performance. Controlled experiments can simulate different conditions, such as reduced power levels or environmental disturbances, to understand how they affect the DWLR readings. The insights from these experiments can then be incorporated into the anomaly detection models to make them more robust in detecting different types of anomalies.

Alternatively, DWLRs can be configured to send additional metadata along with water level readings, such as the current battery percentage. This would make the problem of detecting anomalies related to low battery levels straightforward. With battery information included in the incoming data stream, the system can easily flag DWLRs operating with low power and differentiate between power-related issues and genuine anomalies in the groundwater data.

Similarly, other types of data could be leveraged to improve the anomaly detection system. For example, if we had data on how extreme weather events, mechanical wear, or calibration errors affect DWLR readings, we could enhance the model’s ability to correctly classify the cause of anomalies. This kind of comprehensive, contextual data would allow the system to make more accurate estimates about the underlying reasons for the detected anomalies, leading to better decision-making and more effective resource management.

In conclusion, as more data becomes available—whether through ongoing monitoring, experiments, or additional sensor inputs—the LSTM autoencoder models can become more sophisticated in their ability to detect and explain anomalies. By continually updating the models with new and relevant data, we can significantly improve their accuracy, reduce false positives, and ensure that the appropriate authorities are alerted to the right issues in a timely manner.
