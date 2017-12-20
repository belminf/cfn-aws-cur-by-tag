# sam-aws-cur-by-tag
## Lambda functions

Needs IAM role with:
* S3 access
* Athena
* Lambda basic exec

### 1. get_tags
Desc: Get tags on an Athena update
Trigger: Adding to the Athena CUR folder?
Output: $bucket/tags/$year/$m/<ID>.csv

### 2. query_athena
Desc: Query Athena for tag and month
Trigger: $bucket/tags/\*.csv
Output: $bucket/athena_out/$y/$m/$tag/<ID>.csv

### 3. copy_final_csv
Desc: Copy Athena output to human readable file
Trigger: $bucket/athena_out/\*.csv
Output: $bucket/reports/$tag/$y-$m.csv

## Considerations
* Currently doesn't clean up Athena query output S3 files ($bucket/athena_out and $bucket/tags)
* Doesn't create a report for non-tagged items
* Not sure how it'll do with single digit months; we'll find it in January!
