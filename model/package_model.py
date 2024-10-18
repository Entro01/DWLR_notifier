import tarfile
import os

def create_tar_gz(source_dir, output_filename):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

if __name__ == "__main__":
    model_dir = 'model/saved_model'  # Adjust this path as needed
    output_filename = 'model/lstm_autoencoder.tar.gz'

    create_tar_gz(model_dir, output_filename)
    print(f"Model packaged as {output_filename}")