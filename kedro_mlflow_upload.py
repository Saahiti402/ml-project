import sys
import subprocess
import os
from datetime import datetime

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing {package}: {e}")
        raise

def install_dependencies():
    """Ensure necessary dependencies are installed."""
    install_package("mlflow")
    install_package("kedro")
    install_package("kedro-viz")

def run_kedro_pipeline():
    """Run the Kedro pipeline."""
    try:
        print("🚀 Running Kedro pipeline...")
        subprocess.check_call(["kedro", "run"])
        print("✅ Kedro pipeline ran successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Kedro pipeline: {e}")
        raise

def generate_kedro_viz():
    """Generate Kedro visualization with a timestamped file."""
    try:
        print("🎨 Generating Kedro viz...")

        # Create a timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"my_shareable_pipeline_{timestamp}.json"

        # Make sure the file or folder doesn't exist
        if os.path.exists(output_file):
            if os.path.isdir(output_file):
                print(f"⚠️ Found a directory named {output_file}, deleting it...")
                os.rmdir(output_file)
            else:
                print(f"⚠️ Found an old file named {output_file}, deleting it...")
                os.remove(output_file)

        # Now run the command with the fresh filename
        subprocess.check_call([
            "kedro", "viz", "run", f"--save-file={output_file}"
        ])

        print(f"✅ Kedro viz generated and saved to {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating Kedro visualization: {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise

def main():
    """Main function to orchestrate Kedro run, viz generation, and MLflow upload."""
    try:
        install_dependencies()
        run_kedro_pipeline()
        generate_kedro_viz()
    except Exception as e:
        print(f"❌ Fatal Error: {e}")
        raise

if __name__ == "__main__":
    main()
