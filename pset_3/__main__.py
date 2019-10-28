""" Start of imported code """

from .hash_str import get_csci_salt, get_user_id, hash_str
from .io import atomic_write
from .cli import main
import pandas as pd
import fastparquet
import os


def get_user_hash(username, salt=None):

    salt = salt or get_csci_salt()
    print(salt)
    return hash_str(username, salt=salt)


def call_getuserid():
    for user in [
        get_csci_salt("USER_1", convert_to_bytes="No"),
        get_csci_salt("USER_2", convert_to_bytes="No"),
    ]:
        print("Id for {}: {}".format(user, get_user_id(user)))


def parquet_conv(filename, cwd=os.getcwd(), datasourceformat=".xlsx"):
    parquetfilename = filename + ".parquet"
    data_wd = os.path.abspath(os.path.join(cwd, "data"))
    data_source = os.path.join(data_wd, filename + datasourceformat)
    try:
        df = pd.read_csv(data_source)
    except:
        df = pd.read_excel(data_source)

    atomic_write(fastparquet.write(parquetfilename, df, compression=None))
    result = pd.read_parquet(
        parquetfilename, engine="fastparquet", columns=["hashed_id"]
    )
    print(result)
    return result


if __name__ == "__main__":
    main()
