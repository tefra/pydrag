from vcr import config, VCR

fixture = config.VCR(
    filter_query_parameters=["api_key"],
    cassette_library_dir="fixtures",
    path_transformer=VCR.ensure_suffix(".json"),
    serializer="json",
)
