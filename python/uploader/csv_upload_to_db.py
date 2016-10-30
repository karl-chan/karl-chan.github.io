import argparse
import common.credentials_manager as credmgr
import mysql.connector


class RouteDBUploader(object):
    ''' Uploads downloaded csv file to database '''
    route_ids_url_template = 'https://api.tfl.gov.uk/Line/Mode/bus?' \
                             'app_id={app_id}&app_key={app_key}'
    route_infos_url_template = 'https://api.tfl.gov.uk/Line/{line}' \
                               '/Route/Sequence/{direction}?' \
                               'excludeCrowding=True' \
                               '&app_id={app_id}&app_key={app_key}'

    def __init__(self):
        credentials_manager = credmgr.CredentialsManager()
        mysql_credentials = credentials_manager.get_mysql_credentials()
        self.host = mysql_credentials['host']
        self.db_name = mysql_credentials['db_name']
        self.user = mysql_credentials['user']
        self.password = mysql_credentials['password']

        self.cnx = mysql.connector.connect(user=self.user,
                                           password=self.password,
                                           host=self.host,
                                           database=self.db_name,
                                           autocommit=True)

    def create_table_if_not_exists(self):
        cursor = self.cnx.cursor()
        try:
            cursor.execute('CREATE TABLE IF NOT EXISTS route_info ('
                           '    line VARCHAR(255),'
                           '    direction VARCHAR(255),'
                           '    id VARCHAR(255),'
                           '    name VARCHAR(255),'
                           '    stop_sequence VARCHAR(255),'
                           '    stop_letter VARCHAR(255),'
                           '    towards VARCHAR(255),'
                           '    lat DECIMAL(10,7),'
                           '    lon DECIMAL(10,7),'
                           '    PRIMARY KEY (line, direction, stop_sequence),'
                           '    INDEX route_info_id_idx (id),'
                           '    INDEX route_info_lat_lon_idx (lat, lon)'
                           ')')
        except mysql.connector.Error as err:
            print(err)

    def upload_csv(self, csv_path):
        self.cnx.autocommit = False
        cursor = self.cnx.cursor()
        try:
            cursor.execute('DELETE FROM route_info')
            cursor.execute("""LOAD DATA LOCAL INFILE '{file_path}'
                           INTO TABLE route_info
                           FIELDS TERMINATED BY ','
                           OPTIONALLY ENCLOSED BY '"'
                           LINES TERMINATED BY '\\r\\n'
                           IGNORE 1 LINES""".format(file_path=csv_path))
            self.cnx.commit()
        except:
            self.cnx.rollback()
        self.cnx.autocommit = True


# Code below for main() only
def parseArgs():
    ''' Parses command line arguments for the output file format (json or csv),
        and the output file path '''
    parser = argparse.ArgumentParser()
    parser.add_argument('csv',
                        help='Specify path to csv file')
    args = parser.parse_args()
    return args.csv


if __name__ == '__main__':
    file_path = parseArgs()
    uploader = RouteDBUploader()
    uploader.create_table_if_not_exists()
    uploader.upload_csv(file_path)
