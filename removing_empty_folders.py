databasee = "your_catalog.your_database"
container = "your_container"
storage_account = "your_storage_account"
mount_folder = "your_mount_folder"

for table in spark.sql(f"show tables in {databasee}").collect():
  partitions_to_delete = spark.sql(f"VACUUM {databasee}.{table.tableName} DRY RUN")
  print("checking the empty folders for the table " + table.tableName)
  for partition_to_delete in partitions_to_delete.collect():
    if partition_to_delete.path != "":
      if f"abfss://{container}" in partition_to_delete.path:
        path_to_delete = partition_to_delete.path.replace(f"abfss://{container}@{storage_account}.dfs.core.windows.net", f"dbfs:/mnt/{mount_folder}")
        print("removing the folder " + path_to_delete)
        dbutils.fs.rm(path_to_delete, True)
