# Databricks notebook source
# DBTITLE 1,Set Catalog, Schema, and Create Table
# Set catalog and schema
catalog_name = "adc_agent_copilot_dbx_rsc"
schema_name = "intent_models"
table_name = "learning_transcripts"

# Use existing catalog and schema
spark.sql(f"USE CATALOG {catalog_name}")
spark.sql(f"USE SCHEMA {schema_name}")

# Create table with sample schema
spark.sql(f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    transcript_id STRING,
    speaker_name STRING,
    transcript_text STRING,
    duration_seconds INT
)
USING DELTA
""")

# COMMAND ----------

# DBTITLE 1,Create PHI Masking Function (SQL)
# MAGIC %sql
# MAGIC
# MAGIC
# MAGIC CREATE FUNCTION intent_models.mask_speaker_name_pii_phi(name STRING)
# MAGIC RETURN CASE 
# MAGIC     WHEN is_member('CopilotAdmins') THEN name 
# MAGIC     ELSE 'REDACTED' 
# MAGIC END;
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# DBTITLE 1,Apply Column-Level Masking PHI check
# Apply column-level masking using Unity Catalog masking function
spark.sql(f"""
ALTER TABLE {catalog_name}.{schema_name}.{table_name}
ALTER COLUMN speaker_name
SET MASK {schema_name}.mask_speaker_name_pii_phi
""")


# COMMAND ----------

# DBTITLE 1,Insert Sample Data
from pyspark.sql import Row
from pyspark.sql.types import IntegerType

sample_data = [
    Row(transcript_id="t1", speaker_name="Alice", transcript_text="Hello, welcome to the session.", duration_seconds=12),
    Row(transcript_id="t2", speaker_name="Bob", transcript_text="This is a longer transcript with more content.", duration_seconds=45),
    Row(transcript_id="t3", speaker_name="Charlie", transcript_text="Short one.", duration_seconds=8)
]

df = spark.createDataFrame(sample_data)

# Cast duration_seconds to IntegerType to match table schema
df = df.withColumn("duration_seconds", df["duration_seconds"].cast(IntegerType()))

df.write.mode("append").saveAsTable(f"{catalog_name}.{schema_name}.{table_name}")

# COMMAND ----------

# DBTITLE 1,Export Table to Parquet
df = spark.table(f"{catalog_name}.{schema_name}.{table_name}")
df.write.mode("overwrite").parquet("dbfs:/tmp/learning_transcripts_artifact")

# COMMAND ----------

# DBTITLE 1,Display DBFS Contents
display(dbutils.fs.ls("dbfs:/tmp/learning_transcripts_artifact"))

# COMMAND ----------

# DBTITLE 1,Log Artifact to MLflow (Local Copy)
import mlflow
import os
import shutil

# Define paths
dbfs_path = "/dbfs/tmp/learning_transcripts_artifact"  # DBFS path (accessible via /dbfs)
local_path = "/tmp/learning_transcripts_artifact"      # Local path on driver

# Clean up local path if it already exists
shutil.rmtree(local_path, ignore_errors=True)

# Copy from DBFS to local driver path
if os.path.exists(dbfs_path):
    shutil.copytree(dbfs_path, local_path)

    # Start MLflow run and log artifact
    with mlflow.start_run(run_name="Register Learning Transcript Dataset"):
        mlflow.log_artifact(local_path, artifact_path="dataset")
else:
    print("DBFS path does not exist. Please check if the dataset was written correctly.")


# COMMAND ----------

# DBTITLE 1,Log Artifact to MLflow (Direct DBFS Path)
import mlflow

# Check if DBFS path exists
if len(dbutils.fs.ls("dbfs:/tmp/learning_transcripts_artifact")) > 0:
    with mlflow.start_run(run_name="Register Learning Transcript Dataset"):
        mlflow.log_artifacts("/dbfs/tmp/learning_transcripts_artifact", artifact_path="dataset")
else:
    print("DBFS path does not exist or is empty.")


# COMMAND ----------

# DBTITLE 1,Train and Log ML Model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import numpy as np

# Load data from Delta table
df = spark.table(f"{catalog_name}.{schema_name}.{table_name}").toPandas()

# Label: short (<30s) vs long (>=30s)
df["label"] = df["duration_seconds"].apply(lambda x: 1 if x >= 30 else 0)

# Feature: transcript length
df["text_length"] = df["transcript_text"].apply(len)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(df[["text_length"]], df["label"], test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)

# Provide input example for MLflow
input_example = np.array([[100]])  # Example transcript length

# Log model and metadata to MLflow
with mlflow.start_run(run_name="Transcript Classifier"):
    mlflow.log_metric("accuracy", acc)
    mlflow.log_param("model_type", "LogisticRegression")
    mlflow.log_param("feature", "text_length")
    mlflow.sklearn.log_model(model, "model", input_example=input_example)


# COMMAND ----------

# DBTITLE 1,Load Model and Predict
import numpy as np
import mlflow.sklearn

# Load model from MLflow using run ID
model = mlflow.sklearn.load_model("runs:///0d688840624f49b49864f988b88943c0/model")

# Define a new transcript
new_transcript_text = "Thanks for joining. Let's begin the session on AI and productivity."
text_length = len(new_transcript_text)

# Prepare input
input_data = np.array([[text_length]])

# Predict
prediction = model.predict(input_data)[0]
label = "long" if prediction == 1 else "short"

print(f"Transcript length: {text_length}")
print(f"Predicted label: {label}")

# COMMAND ----------

# DBTITLE 1,Register Model (Manual)
import mlflow

model_name = "TranscriptLengthClassifier-Learning-only-Non-Production"

run_id = "0d688840624f49b49864f988b88943c0"   
model_uri = f"runs:/{run_id}/model"


# Register the model
mlflow.register_model(model_uri=model_uri, name=model_name)

# COMMAND ----------

# DBTITLE 1,Register Model (Inline)
import mlflow
import mlflow.sklearn
import numpy as np

input_example = np.array([[100]])  # Example input

with mlflow.start_run(run_name="Transcript Classifier"):
    mlflow.log_metric("accuracy", acc)
    mlflow.log_param("model_type", "LogisticRegression")
    mlflow.log_param("feature", "text_length")
    
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        input_example=input_example,
        registered_model_name="adc_agent_copilot_dbx_rsc.intent_models.TranscriptLengthClassifier"
    )