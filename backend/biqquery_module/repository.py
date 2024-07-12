from google.cloud import bigquery
from fastapi import HTTPException, Depends
import logging
import sys
import os
sys.path.append('.')
from config import settings

client = bigquery.Client()
logger = logging.getLogger('uvicorn.error')

def get_all_countries():
    dataset_str = f"{settings.PROJECT_ID}.{settings.DATASET_ID}.{settings.TABLE_ID}"
    query = f"SELECT * FROM {dataset_str};"
    logger.info("Start querying data form Biq Query!")
    try:
        query_job = client.query(query)
        query_results = query_job.result()
    
        result_list = [dict(row) for row in query_results]
        logger.info("Job has successfully finished!")
        return result_list
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(ex)}")   

