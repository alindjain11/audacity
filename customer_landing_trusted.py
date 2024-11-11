import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1731317766051 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://udacity11/customer/landing/"], "recurse": True}, transformation_ctx="AmazonS3_node1731317766051")

# Script generated for node Privacy Filter
SqlQuery8779 = '''
select * from myDataSource
where shareWithResearchAsOfDate is not null
'''
PrivacyFilter_node1731329726399 = sparkSqlQuery(glueContext, query = SqlQuery8779, mapping = {"myDataSource":AmazonS3_node1731317766051}, transformation_ctx = "PrivacyFilter_node1731329726399")

# Script generated for node Customer Trusted Zone
CustomerTrustedZone_node1731318371918 = glueContext.getSink(path="s3://udacity11/customer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="CustomerTrustedZone_node1731318371918")
CustomerTrustedZone_node1731318371918.setCatalogInfo(catalogDatabase="stedi11",catalogTableName="customer_trusted")
CustomerTrustedZone_node1731318371918.setFormat("json")
CustomerTrustedZone_node1731318371918.writeFrame(PrivacyFilter_node1731329726399)
job.commit()