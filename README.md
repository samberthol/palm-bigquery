# Google PaLM on BigQuery with LangChain

This project intends to provide a quick way to integrate **PaLM** with **BigQuery** in Python, using **SQLAlchemy** and **LangChain** to glue together the pieces. This is in no way a production ready artefact, it rather provides a proof of concept for testing purposes.

The inception of this project was to evaluate if BigQuery could be interrogated using an LLM. The results were rather satisfying, hence the publication. While not provided here, the integration with **ChatGPT** worked as well and can be switched with PaLM easily. 

## Architecture Design

image

## Components

**PaLM 2** is the latest LLM provided by Google as a cloud service that is quite performant and easy to access through [API](https://developers.generativeai.google/api/python/google/generativeai) using Python. Note that at the moment writing this, PaLM is not widely available in Europe and you may need to access it through a server/services in the US. 

[BigQuery](https://cloud.google.com/bigquery/docs/introduction) is a powerful managed DataWarehouse that provides an out of the box and serverless analytical database. Users often use it to store vast amounts of Data. In this example, we have used the following public and free [Thelook](https://console.cloud.google.com/bigquery/analytics-hub/exchanges;cameo=analyticshub;pageName=listing-detail;pageResource=1057666841514.us.google_cloud_public_datasets_17e74966199.thelook_ecommerce) Dataset.

[LangChain](https://python.langchain.com/docs/get_started/introduction) provides an OSS suite of building blocks to chain LLM oriented tasks with reasoning like database queries, math, document loaders, vector dbs or parsers.

[SQL Alchemy](https://www.sqlalchemy.org/) is a Python toolkit to provide an abstract layer to many popular databases.

## Setup

### Prerequisites
In order to launch the script you will need the following :
- A working [Python 3](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) environment
- Install dependencies using pip
- A Google [PaLM API key](https://developers.generativeai.google/tutorials/setup)
- A [service account](https://cloud.google.com/iam/docs/service-account-overview) on Google Cloud with [BigQuery Data Viewer](https://cloud.google.com/bigquery/docs/access-control-basic-roles)rights and download the [JSON key file](https://cloud.google.com/iam/docs/keys-create-delete).
- [BigQuery API](https://console.cloud.google.com/marketplace/product/google/bigquery.googleapis.com) needs to be activated.

### Deploy

To install the dependencies, you will need to run the following command
```
pip install langchain openai chromadb tiktoken tabulate sqlalchemy sqlalchemy-bigquery google-cloud-bigquery google-generativeai
```

### Set variables
```
service_account_file = "your_sa_account_key_file.json"
os.environ['GOOGLE_API_KEY'] = 'your_palm_api_key'
project = "your_project_id" 
dataset = "your_dataset" # Defined when you imported TheLook Dataset
table = "you_table"
```
Notes
The JSON service account key file should be accessible to your script.
The variable `your_project_id` can be found [here](https://console.cloud.google.com/home/dashboard). The variable `your_dataset` is defined when you import TheLook dataset from AnalyticsHub. You can set `your_table` to the `orders` table from TheLook.

### Running the script
You can run the script using the following command
```
python3 launcher-PaLM.py
```

Example output
```
Entering new AgentExecutor chain...
Action: sql_db_list_tables
Action Input: 
Observation: events
Thought:events is a relevant table.  I should query the schema of events to see what columns I can use.
Action: sql_db_schema
Action Input: events
Observation: 
CREATE TABLE `events` (
	`user_id` INT64, 
	`sequence_number` INT64, 
	`session_id` STRING, 
	`created_at` TIMESTAMP, 
	`ip_address` STRING, 
	`city` STRING, 
	`state` STRING, 
	`postal_code` STRING, 
	`browser` STRING, 
	`uri` STRING, 
	`event_type` STRING, 
	`ide` INT64, 
	`traffic_sources` STRING
)

/*
3 rows from events table:
user_id	sequence_number	session_id	created_at	ip_address	city	state	postal_code	browser	uri	event_type	ide	traffic_sources
41525	4	c75439e0-127d-4721-be6c-b03af9255b3f	2020-10-31 16:57:38+00:00	118.90.172.146	Bogatynia	Dolnośląskie	59	Chrome	/cart	cart	539126	Email
None	3	2fc7f38e-d997-4c26-b493-48ad47aaf8b0	2022-04-07 02:35:00+00:00	83.132.130.52	Bogatynia	Dolnośląskie	59	Safari	/cart	cart	2271896	Adwords
None	3	e35a5c16-85e2-412a-8226-5fe9285ab994	2021-12-29 03:09:00+00:00	162.176.5.118	Bogatynia	Dolnośląskie	59	Chrome	/cart	cart	2148147	Email
*/
Thought:The traffic_sources column contains the publisher sources.  I should group the results by traffic_sources and order by count desc.
Action: sql_db_query
Action Input: SELECT traffic_sources, count(*) AS count FROM events GROUP BY traffic_sources ORDER BY count DESC LIMIT 3
Observation: [('Email', 1092153), ('Adwords', 730558), ('Facebook', 243532)]
Thought:I now know the final answer
Final Answer: The top 3 publisher sources are Email, Adwords, and Facebook.

> Finished chain.
'The top 3 publisher sources are Email, Adwords, and Facebook.'
```

## Comments
One great features of SQL Alchemy with LangChain is that you do not need to setup a schema as it is created on the fly.
The `temperature` can be adjusted to throttle the "creativity" of your LLM. The `top_k` can be adjusted according to the token size accepted by your API.
You can add a UI easily with Gradio or Strimlit on top of your project