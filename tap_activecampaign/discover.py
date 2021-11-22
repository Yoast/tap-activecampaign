import singer
from singer.catalog import Catalog, CatalogEntry, Schema
from tap_activecampaign.schema import get_schemas
from tap_activecampaign.streams import flatten_streams

LOGGER = singer.get_logger()

def discover():
    LOGGER.info('~~~~~Made it to discover.py discover function head~~~~~')
    schemas, field_metadata = get_schemas()
    LOGGER.info('~~~~~Made it to discover.py after get_schemas call~~~~~')
    catalog = Catalog([])
    LOGGER.info('~~~~~Made it to discover.py after catalog call~~~~~')

    flat_streams = flatten_streams()
    for stream_name, schema_dict in schemas.items():
        LOGGER.info('~~~~~Made it to discover.py inside flatten_streams for loop~~~~~')
        try:
            schema = Schema.from_dict(schema_dict)
            mdata = field_metadata[stream_name]
        except Exception as err:
            LOGGER.error(err)
            LOGGER.error('stream_name: {}'.format(stream_name))
            LOGGER.error('type schema_dict: {}'.format(type(schema_dict)))
            raise err

        catalog.streams.append(CatalogEntry(
            stream=stream_name,
            tap_stream_id=stream_name,
            key_properties=flat_streams.get(stream_name, {}).get('key_properties', None),
            schema=schema,
            metadata=mdata
        ))

    return catalog
