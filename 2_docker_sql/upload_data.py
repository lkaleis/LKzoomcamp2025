#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from time import time


# In[5]:


pwd


# In[8]:


df = pd.read_csv('/home/lpop22/LKzoomcamp2025/2_docker_sql/yellow_tripdata_2021-01.csv.gz', nrows=100)


# In[15]:


df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


# In[9]:


df.head()


# In[22]:


engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[23]:


engine.connect()


# In[16]:


pd.io.sql.get_schema(df, name='yellow_taxi_data')


# In[30]:


df_iter = pd.read_csv('/home/lpop22/LKzoomcamp2025/2_docker_sql/yellow_tripdata_2021-01.csv.gz', iterator=True, chunksize=10000)


# In[31]:


df = next(df_iter)


# In[32]:


df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


# In[33]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[25]:


#%time df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[35]:


while True:
    
    try:
        t_start = time()
    
        df = next(df_iter)
    
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    
        df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
    
        t_end = time()
    
        print('inserted another chunk, took %.3f second' % (t_end - t_start))
    except StopIteration:
        print("finished ingesting data into postgres db")
        break


# In[37]:


query = """
SELECT count(*) FROM yellow_taxi_data
"""

pd.read_sql(query, con = engine)

