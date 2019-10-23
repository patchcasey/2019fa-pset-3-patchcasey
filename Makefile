.PHONY: data 46a4bb62

HASH_ID:
	46a4bb62

data: 
	data/project.parquet
	data/vectors.npy.gz
	data/words.txt

data/project.parquet:
	aws s3 cp s3://cscie29-data/46a4bb62/pset_3/project.parquet data/ --request-payer=requester
	
data/vectors.npy.gz:
	aws s3 cp s3://cscie29-data/46a4bb62/pset_3/vectors.npy.gz data/ --request-payer=requester
	
data/words.txt:	
	aws s3 cp s3://cscie29-data/46a4bb62/pset_3/words.txt data/ --request-payer=requester