import sys
import subprocess
import os
import time
import zipfile
from datetime import datetime

import mlflow
import shutil
from datetime import datetime


def install_dependencies():
    print("🔧 Installing dependencies from requirements.txt...")
    subprocess.check_call(["pip3", "install", "-r", "requirements.txt"])


def generate_kedro_viz():
    print("📈 Generating Kedro pipeline visualization...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"my_shareable_pipeline_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    subprocess.check_call([
        "kedro", "viz", "--save-file", os.path.join(output_dir, "pipeline.json")
    ])
    return output_dir


def compress_output(output_dir):
    print("🗜️ Compressing the visualization directory...")

    # Check if the directory exists before proceeding
    if not os.path.exists(output_dir):
        print(f"❌ Error: Directory {output_dir} does not exist!")
        return None

    zip_filename = f"{output_dir}.zip"
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=output_dir)
                print(f"Adding {file_path} as {arcname}")  # Debugging line
                zipf.write(file_path, arcname)

    # Verify if the zip file was created
    if os.path.exists(zip_filename):
        print(f"✅ Successfully compressed into {zip_filename}")
        return zip_filename
    else:
        print(f"❌ Failed to create zip file: {zip_filename}")
        return None


def upload_to_mlflow(zip_filename):
    if zip_filename is None:
        print("❌ No zip file to upload!")
        return
    print("🚀 Uploading the artifact to MLflow...")
    mlflow.set_experiment("kedro_viz_artifacts")
    with mlflow.start_run(run_name="kedro_viz_upload") as run:
        mlflow.log_artifact(zip_filename, artifact_path="kedro_viz_output")
    print(f"✅ Upload successful! Run ID: {run.info.run_id}")


def clean_up(output_dir, zip_filename):
    print("🧹 Cleaning up temporary files...")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    if os.path.exists(zip_filename):
        os.remove(zip_filename)


def main():
    try:
        install_dependencies()
        output_dir = generate_kedro_viz()
        zip_filename = compress_output(output_dir)
        if zip_filename:
            upload_to_mlflow(zip_filename)
    except subprocess.CalledProcessError as e:
        print(f"❌ Subprocess failed: {e}")
    except Exception as ex:
        print(f"❌ An error occurred: {ex}")
    finally:
        # Always clean up even if error
        try:
            clean_up(output_dir, zip_filename)
        except Exception:
            pass


if __name__ == "__main__":
    main()
