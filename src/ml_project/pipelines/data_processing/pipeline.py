from kedro.pipeline import Pipeline, node
from .nodes import load_data, clean_data

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=load_data,
                inputs=None,
                outputs="raw_data",
                name="load_data_node",
            ),
            node(
                func=clean_data,
                inputs="raw_data",
                outputs="cleaned_data",
                name="clean_data_node",
            ),
        ]
    )
