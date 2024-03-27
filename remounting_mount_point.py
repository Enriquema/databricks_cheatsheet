key = dbutils.secrets.get(scope="credentials", key="SP-Password")
id = dbutils.secrets.get(scope="credentials",key="clientId")

# prepare extra configs of ADLS Gen 1 + 2
configsGen1 = {"dfs.adls.oauth2.access.token.provider.type": "ClientCredential",
	"dfs.adls.oauth2.client.id": id ,
	"dfs.adls.oauth2.credential": key,
	"dfs.adls.oauth2.refresh.url": "https://login.microsoftonline.com/9652d7c2-1ccf-4940-8151-4a92bd474ed0/oauth2/token"}

configsGen2 = {"fs.azure.account.auth.type": "OAuth",
	"fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
	"fs.azure.account.oauth2.client.id": id,
	"fs.azure.account.oauth2.client.secret": key,
	"fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/9652d7c2-1ccf-4940-8151-4a92bd474ed0/oauth2/token"}

# process mount points
mountpoints = dbutils.fs.mounts()
for mountpoint in mountpoints:
	if mountpoint.source.startswith('adl://xto'):
		print("Remounting (Unmount and mounting) ADLS Gen 1 mount point: " + mountpoint.mountPoint + ', source: ' + mountpoint.source)
		dbutils.fs.unmount(mount_point=mountpoint.mountPoint)
		dbutils.fs.mount(mount_point=mountpoint.mountPoint, source=mountpoint.source, extra_configs=configsGen1)
	elif mountpoint.source.startswith('abfss://'):
		print("Remounting (Unmount and mounting) ADLS Gen 2 mount point: " + mountpoint.mountPoint + ', source: ' + mountpoint.source)
		dbutils.fs.unmount(mount_point=mountpoint.mountPoint)
		dbutils.fs.mount(mount_point=mountpoint.mountPoint, source=mountpoint.source, extra_configs=configsGen2)
	else:
		print("Ignoring NON-ADLS mount point: " + mountpoint.mountPoint + ', source: ' + mountpoint.source)
