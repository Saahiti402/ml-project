from kedro.pipeline import Pipeline
from ml_project.pipelines.data_processing import pipeline as dp

def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines."""
    return {
        "__default__": dp.create_pipeline(),  # Register the data_processing pipeline as the default pipeline
    }
