import os

from vcr import config, VCR

where_am_i = os.path.dirname(os.path.realpath(__file__))


fixture = config.VCR(
    filter_query_parameters=["api_key"],
    cassette_library_dir=os.path.join(where_am_i, "fixtures"),
    path_transformer=VCR.ensure_suffix(".json"),
    serializer="json",
)
