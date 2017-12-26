# sam-aws-cur-by-tag

## Setup
Essentially, you need to setup the cost allocation tag, the CUR report, partitioning of that data and deploy these Lambda functions via SAM to get this running.

### Cost allocation tag
This could be configured on your AWS Billing Console. See [AWS documentation](http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html) for details.

### Cost and Usage report (CUR)
This could also be configured on your AWS Billing Console or via the CLI. The important variables:

* Report name (`$CUR_NAME`): Just has to be unique
* Time unit (`$TIME_UNIT`, Values: `HOURLY`, `DAILY`): Units to use for report
* S3 bucket for CUR (`$CUR_BUCKET`): Existing bucket for your CUR data

For CLI, this is what it would look like:

```bash
$ CUR_NAME=cur_foobar
$ TIME_UNIT=HOURLY
$ CUR_BUCKET=my_cur_bucket

$ aws cur put-report-definition --report-definition 'ReportName=$CUR_NAME,S3Bucket=$CUR_BUCKET,TimeUnit=$TIME_UNIT,Format=textORcsv,Compression=GZIP,AdditionalSchemaElements=RESOURCES,S3Prefix="",S3Region=us-east-1,AdditionalArtifacts=QUICKSIGHT'
```

### Athena partitioning of CUR data
See this [AWS blog post](https://aws.amazon.com/blogs/big-data/query-and-visualize-aws-cost-and-usage-data-using-amazon-athena-and-amazon-quicksight/) for how to configure this with a CloudFormation stack that takes your CUR data and partitions it for Athena.

Note that Setting up the Amazon Quicksight visualizations as discussed on the post is not required.

The CloudFormation has 3 parameters that are worth taking a note of:

* `CostnUsageReport`: Name of your CUR report (`$CUR_NAME` from previous step)
* `S3BucketName`: Bucket where your Athena CUR data is partitioned	
* `s3CURBucket`: Bucket where your original CUR reports are saved by AWS (`$CUR_BUCKET` from previous step)

### Deploy the Lambda functions
Finally, you could deploy this stack using SAM. The stack consist of an S3 bucket and 3 Lambda functions:

1. `get_tags`: Exports the values of the cost allocation tag you want to breakup your report by.
2. `query_athena`: Queries Athena for line-items with each value of the cost allocation tag you chose.
3. `copy_final_csv`: Copies the reports to the S3 bucket you want to store the final output.

There are two parameters that are important:
* `TagKeyParam`: The cost allocation tag you want to breakup your reports by.
* `OutputBucketParam`: The S3 bucket to save the broken up reports.

## Considerations
* **Important:** Lambda IAM role is way too open, could be locked down significantly
* I'm assuming us-east-1 everywhere right now so you may need to change a few things if you're using another region
* Currently doesn't clean up Athena query output S3 files ($bucket/athena_out and $bucket/tags)
* Doesn't create a report for non-tagged items
* Not sure how it'll do with single digit months; we'll find it in January!
