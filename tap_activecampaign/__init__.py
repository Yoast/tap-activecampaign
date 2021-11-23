import sys
import json
import argparse
import singer
from singer import metadata, utils
from tap_activecampaign.client import ActiveCampaignClient
from tap_activecampaign.discover import discover
from tap_activecampaign.sync import sync

LOGGER = singer.get_logger()

REQUIRED_CONFIG_KEYS = [
    'api_url',
    'api_token',
    'start_date',
    'user_agent'
]

def do_discover():

    LOGGER.info('Starting discover')
    catalog = discover()
    LOGGER.info('~~~~~Made it out of discover function call~~~~~')
    LOGGER.info('catalog data: {}'.format(catalog))
    json.dump(catalog.to_dict(), sys.stdout, indent=2)
    LOGGER.info('Finished discover')


@singer.utils.handle_top_exception(LOGGER)
def main():
    LOGGER.info('~~~~~Made it to init.py main~~~~~')
    parsed_args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    with ActiveCampaignClient(parsed_args.config['api_url'],
                              parsed_args.config['api_token'],
                              parsed_args.config['user_agent']) as client:

        state = {}
        if parsed_args.state:
            LOGGER.info('~~~~~Made it to init.py state if statement~~~~~')
            state = parsed_args.state

        if parsed_args.discover:
            LOGGER.info('~~~~~Made it to init.py discocver if statement~~~~~')
            discovered_catalog = do_discover()
            sync(client=client,
                 config=parsed_args.config,
                 catalog=discovered_catalog,
                 state=state)
        elif parsed_args.catalog:
            LOGGER.info('~~~~~Made it to init.py else catalog statement~~~~~')
            sync(client=client,
                 config=parsed_args.config,
                 catalog=parsed_args.catalog,
                 state=state)

if __name__ == '__main__':
    main()
