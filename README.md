# sam-aws-cur-by-tag

## Setup
0. Deploy SAM template
1. Create stack that takes CUR data and partitions it for Athena
2. Create Lambda triggers for functions below

## Lambda functions

### 1. get_tags
Get tags on an Athena update

* Trigger: $athena_bucket/year=\*/month=\*/\*.csv
* Output: $bucket/tags/$year/$m/<ID>.csv

### 2. query_athena
Query Athena for tag and month

* Trigger: $bucket/tags/\*.csv
* Output: $bucket/athena_out/$y/$m/$tag/<ID>.csv

### 3. copy_final_csv
Copy Athena output to human readable file

* Trigger: $bucket/athena_out/\*.csv
* Output: $bucket/reports/$tag/$y-$m.csv

## Considerations
* **Important:** Lambda IAM role is way too open, could be locked down significantly
* Currently doesn't clean up Athena query output S3 files ($bucket/athena_out and $bucket/tags)
* Doesn't create a report for non-tagged items
* Not sure how it'll do with single digit months; we'll find it in January!
