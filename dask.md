# Dask

## Comparison to Spark 

### Reasons you might choose Spark
You prefer Scala or the SQL language
You have mostly JVM infrastructure and legacy systems
You want an established and trusted solution for business
You are mostly doing business analytics with some lightweight machine learning
You want an all-in-one solution

### Reasons you might choose Dask
You prefer Python or native code, or have large legacy code bases that you do not want to entirely rewrite
Your use case is complex or does not cleanly fit the Spark computing model
You want a lighter-weight transition from local computing to cluster computing
You want to interoperate with other technologies and don't mind installing multiple packages

### Reasons to choose both
It is easy to use both Dask and Spark on the same data and on the same cluster.

They can both read and write common formats, like CSV, JSON, ORC, and Parquet, making it easy to hand results off between Dask and Spark workflows.

They can both deploy on the same clusters. Most clusters are designed to support many different distributed systems at the same time, using resource managers like Kubernetes and YARN. If you already have a cluster on which you run Spark workloads, it's likely easy to also run Dask workloads on your current infrastructure and vice versa.

In particular, for users coming from traditional Hadoop/Spark clusters (such as those sold by Cloudera/Hortonworks) you are using the Yarn resource manager. You can deploy Dask on these systems using the Dask Yarn project, as well as other projects, like JupyterHub on Hadoop.
