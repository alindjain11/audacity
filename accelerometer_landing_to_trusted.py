import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Customer Trusted
CustomerTrusted_node1731340528189 = glueContext.create_dynamic_frame.from_catalog(database="stedi11", table_name="customer_trusted", transformation_ctx="CustomerTrusted_node1731340528189")

# Script generated for node Accelerometer Landing
AccelerometerLanding_node1731340482489 = glueContext.create_dynamic_frame.from_catalog(database="stedi11", table_name="accelerometer_landing", transformation_ctx="AccelerometerLanding_node1731340482489")

# Script generated for node Join
Join_node1731340582937 = Join.apply(frame1=AccelerometerLanding_node1731340482489, frame2=CustomerTrusted_node1731340528189, keys1=["user"], keys2=["email"], transformation_ctx="Join_node1731340582937")

# Script generated for node Drop Fields
DropFields_node1731342154636 = ApplyMapping.apply(frame=Join_node1731340582937, mappings=[("user", "string", "user", "string"), ("timestamp", "long", "timestamp", "long"), ("x", "float", "x", "float"), ("y", "float", "y", "float"), ("z", "float", "z", "float")], transformation_ctx="DropFields_node1731342154636")

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1731340643472 = glueContext.getSink(path="s3://udacity11/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], compression="snappy", enableUpdateCatalog=True, transformation_ctx="AccelerometerTrusted_node1731340643472")
AccelerometerTrusted_node1731340643472.setCatalogInfo(catalogDatabase="stedi11",catalogTableName="accelerometer_trusted")
AccelerometerTrusted_node1731340643472.setFormat("json")
AccelerometerTrusted_node1731340643472.writeFrame(DropFields_node1731342154636)
job.commit()