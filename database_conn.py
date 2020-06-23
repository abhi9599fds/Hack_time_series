import ibm_db_dbi

class Database_write:
    def __init__(self):
        self.str_conn="DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-07.services.eu-gb.bluemix.net;" \
                      "PORT=50000;PROTOCOL=TCPIP;UID=bfr48077;PWD=3j4h-zwx77mzftr4"
    def insert_dump(self,df_ne):
        try:
            conn = ibm_db_dbi.connect(self.str_conn, " ", " ")
            cur = conn.cursor()
            for i in range(df_ne.shape[0]):
                cur.execute("insert into dump_data values(?,?,?,?,?,?)",(df_ne.index[i],
                            df_ne.iloc[i,0],df_ne.iloc[i,1],df_ne.iloc[i,2],df_ne.iloc[i,3],df_ne.iloc[i,4]))
            conn.commit()
            return True
        except Exception as ex:
            print(ex)
            print(ex.args)
            return False
        finally:
            conn.close()
    def insert_12hrs(self,df_ne):
        pass