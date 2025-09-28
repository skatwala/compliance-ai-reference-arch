# Databricks notebook source
# DBTITLE 1,Define Audio File Path
# Path to the uploaded audio file in DBFS
audio_path = "/dbfs/FileStore/audio/test_audio_file.wav"

# COMMAND ----------

# DBTITLE 1,Install Open AI SDK
# MAGIC %pip install --upgrade openai

# COMMAND ----------

# DBTITLE 1,Transcribe Audio Using Whisper
import openai

api_key=dbutils.secrets.get(scope="dev-kv", key="ADC-OPENAI-EUS2-API-KEY")

# Set your OpenAI API key
openai.api_key = api_key; 
client = openai.OpenAI(api_key=api_key)

# Local audio file path (already copied from Volume)
local_audio_path = "/tmp/test-audio-file.wav"

# Transcribe using Whisper V1 API
with open(local_audio_path, "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

transcript_text = transcript.text
print(transcript_text)

# COMMAND ----------

# DBTITLE 1,Create DataFrame and Save to Delta Table
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

# Create a DataFrame with metadata
df = spark.createDataFrame([
    ("test_audio_file.wav", transcript_text)
], ["filename", "transcript"])

# Add ingestion timestamp
df = df.withColumn("ingested_at", current_timestamp())

# Save to Delta table (create if not exists)
df.write.format("delta").mode("append").saveAsTable("audio_transcripts")


# COMMAND ----------

# DBTITLE 1,Write to Table for Audit/Traceabiliaty
df.write.format("delta").mode("append").saveAsTable("audio_transcripts_1")

# COMMAND ----------

# DBTITLE 1,Query Transcripts
# MAGIC %sql
# MAGIC SELECT * FROM audio_transcripts ORDER BY ingested_at DESC;