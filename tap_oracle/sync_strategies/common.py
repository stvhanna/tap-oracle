import singer
import decimal
import datetime
import dateutil.parser
from singer import  metadata

def should_sync_column(metadata, field_name):
   if metadata.get(('properties', field_name), {}).get('inclusion') == 'unsupported':
      return False

   if metadata.get(('properties', field_name), {}).get('selected'):
      return True

   if metadata.get(('properties', field_name), {}).get('inclusion') == 'automatic':
      return True

   if metadata.get(('properties', field_name), {}).get('selected') == False:
      return False

   if metadata.get(('properties', field_name), {}).get('selected-by-default'):
      return True

   return False

def send_schema_message(stream, bookmark_properties):
   s_md = metadata.to_map(stream.metadata)
   if s_md.get((), {}).get('is-view'):
      key_properties = s_md.get((), {}).get('view-key-properties')
   else:
      key_properties = s_md.get((), {}).get('table-key-properties')

   schema_message = singer.SchemaMessage(stream=stream.stream,
                                         schema=stream.schema.to_dict(),
                                         key_properties=key_properties,
                                         bookmark_properties=bookmark_properties)
   singer.write_message(schema_message)
