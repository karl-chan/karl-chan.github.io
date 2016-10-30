import argparse
import json
import requests
import grequests
import common.credentials_manager as credmgr
import pandas as pd
import time
import collections


class RouteDownloader:
    ''' Downloads list of bus routes from tfl '''
    route_ids_url_template = 'https://api.tfl.gov.uk/Line/Mode/bus?' \
                             'app_id={app_id}&app_key={app_key}'
    route_infos_url_template = 'https://api.tfl.gov.uk/Line/{line}' \
                               '/Route/Sequence/{direction}?' \
                               'excludeCrowding=True' \
                               '&app_id={app_id}&app_key={app_key}'

    tfl_requests_per_minute = 300

    def __init__(self, route_ids):
        credentials_manager = credmgr.CredentialsManager()
        tfl_credentials = credentials_manager.get_tfl_credentials()
        self.app_id = tfl_credentials['app_id']
        self.app_key = tfl_credentials['app_key']

        self.route_ids = route_ids if route_ids else self.download_route_ids()
        self.route_infos = self.download_route_infos()

    def download_route_ids(self):
        ''' Returns all bus route ids as a python list'''
        url = self.route_ids_url_template.format(app_id=self.app_id,
                                                 app_key=self.app_key)
        response = requests.get(url)
        response.raise_for_status()
        raw_json = json.loads(response.text)
        route_ids = [data['id'] for data in raw_json]
        return route_ids

    def download_route_infos(self):
        ''' Returns bus route information as pandas dataframe '''
        urls = [self.route_infos_url_template.format(line=route,
                                                     direction=direction,
                                                     app_id=self.app_id,
                                                     app_key=self.app_key)
                for route in self.route_ids
                for direction in ['outbound', 'inbound']]

        batch_size = self.tfl_requests_per_minute
        responses = []

        # Responses fail occasionally, so we retry until all responses are retrieved.
        url_queue = collections.deque(urls)
        while url_queue:
            url_batch = [url_queue.popleft()
                         for _ in range(min(len(url_queue), batch_size))]
            reqs = [grequests.get(url) for url in url_batch]
            resps = grequests.map(reqs)
            responses.extend([r.text for r in resps if r and r.status_code == requests.codes.ok])
            url_queue.extend([url_batch[i] for i, r in enumerate(resps) if not r])

            [r.close for r in resps if r]

            self.print_update(responses, urls)
            time.sleep(60)

        route_info_dfs = [self.df_from_response(r) for r in responses]
        route_infos_df = pd.concat(route_info_dfs)
        route_infos_df.sort_values(['line', 'direction', 'stop_sequence'], inplace=True)
        return route_infos_df

    def print_update(self, responses, urls):
        ''' Prints the ratio of succesful requests so far, as the download is a
            time consuming process'''
        percentage_complete = int(len(responses) / len(urls) * 100)
        hint_str = '(Update in another minute)' if percentage_complete < 100 else ''
        print('{pc}% complete\t{hint}'.format(pc=percentage_complete,
                                             hint=hint_str))

    def df_from_response(self, response):
        ''' Casts tfl route information json response into python dataframe '''
        dict = json.loads(response)
        line = dict['lineId']
        direction = dict['direction']
        if not dict['stopPointSequences']:
            return None

        route_info_json = json.dumps(dict['stopPointSequences'][0]['stopPoint'])
        route_info_df = pd.read_json(route_info_json, orient='records')
        route_info_df['line'] = line
        route_info_df['direction'] = direction
        route_info_df['stop_sequence'] = route_info_df.index
        route_info_df.rename(columns={'stopLetter': 'stop_letter'}, inplace=True)
        route_info_df = route_info_df[['line', 'direction', 'id', 'name',
                                      'stop_sequence', 'stop_letter', 'towards', 'lat', 'lon']]
        return route_info_df

    def as_df(self):
        ''' Returns bus route information as Pandas dataframe '''
        return self.route_infos

    def as_json(self, path, **kw):
        ''' Returns bus route information as json object '''
        self.route_infos.to_json(path, orient='records')

    def as_csv(self, path, **kw):
        ''' Returns bus route information as csv '''
        self.route_infos.to_csv(path, index=False, **kw)


# Code below for main() only
def parseArgs():
    ''' Parses command line arguments for the output file format (json or csv),
        and the output file path '''
    parser = argparse.ArgumentParser()
    parser.add_argument('format',
                        choices=['json', 'csv'],
                        help='Specify output format (either json or csv)')
    parser.add_argument('path',
                        help='Specify output location')
    parser.add_argument('--routes',
                        nargs='*',
                        help='Download for only these routes')
    args = parser.parse_args()
    return args.format, args.path, args.routes


if __name__ == '__main__':
    file_format, file_path, routes = parseArgs()
    downloader = RouteDownloader(routes)
    switcher = {
        'json': downloader.as_json,
        'csv': downloader.as_csv
    }
    switcher.get(file_format)(file_path)
