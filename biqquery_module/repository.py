from google.cloud import bigquery
from fastapi import HTTPException
import logging
import sys
import os
sys.path.append('.')
from config import dataset_str

client = bigquery.Client()
logger = logging.getLogger('uvicorn.error')
 
def get_all_countries():
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

