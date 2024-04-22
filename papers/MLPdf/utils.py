#!/usr/bin/env python3

from __future__ import annotations
import os, sys, csv, urllib.request, shutil, tarfile, zipfile, logging
from pathlib import Path
sys.path.append(Path.cwd().as_posix())
from datetime import datetime
from typing import TextIO, Dict, List
from dataclasses import dataclass

from pandas import DataFrame


LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "_logs")
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


@dataclass
class PDFMalicious():
   BENIGN_URL = "http://205.174.165.80/CICDataset/CIC-EvasivePDF2022/Dataset/Benign.zip"
   MALICIOUS_URL = "http://205.174.165.80/CICDataset/CIC-EvasivePDF2022/Dataset/Malicious.zip"

def unpack_zip_file_save() -> TextIO:
   pass

class DataTransformations(PDFMalicious):
    def __init__(self, pdf_type: str, ftype: int, split_ratio=0.8) -> DataFrame:
        super(DataTransformations, self).__init__()
        self.curr_path = Path(__file__).resolve().parent.parent.parent
        self.header = ['id', 'label', 'name', 'contents']
        self.pdf_type = pdf_type
        self.ftype = ftype
        self.split_ratio = split_ratio
        self.id_counter = 0
        self.update = []

    @classmethod
    def benign_files(cls) -> Dict: return {"name": "Benign", "type": 0}
   
    @classmethod
    def malicious_files(cls) -> Dict: return {"name": "Malicious", "type": 1}

    @property
    def __str__(self) -> str: return "\n".join(self.update)

    def download_latest_data(self) -> None:
        urllib.request.urlretrieve(self.BENIGN_URL, self.base / 'datasets/benign.zip')
        urllib.request.urlretrieve(self.MALICIOUS_URL, self.base / 'datasets/malicious.zip')
        local_file = 'rps.zip'
        zip_ref = zipfile.ZipFile(local_file, 'r')
        zip_ref.extractall('data/')
        zip_ref.close()

    def extract_tar_file(self) -> str:
        dpath = Path(f"{self.curr_path}/data")
        if not dpath.is_dir():
            os.makedirs(dpath, exist_ok=True)

        fpath = Path(f"{dpath}/{self.pdf_type}")
        tar_path = Path(f"{fpath}/{self.pdf_type}.tar.gz")
        if not tar_path.exists():
            return f"File not found: {tar_path}"

        try:
            file = tarfile.open(tar_path)
            file.extractall(self.curr_path / "data")
            file.close()
            os.remove(tar_path)

            extracted_path = Path(os.path.join(
                self.curr_path, f"data/{self.pdf_type}"))
            index = 1
            for filename in os.listdir(extracted_path):
                old_path = os.path.join(extracted_path / filename)
                new_path = os.path.join(
                    extracted_path, f"{self.pdf_type}_{index}.zip")
                os.rename(old_path, new_path)
                index += 1
            return f"Extraction {self.pdf_type}.tar.gz completed successfully"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, )
            return f"An error occurred: In line [{exc_tb.tb_lineno}] {str(e)}"

    def zip_extract(self) -> str:
        # initialize folder path
        fpath = Path(f"{self.curr_path}/data/{self.pdf_type}")

        try:
            for filename in os.listdir(fpath):
                if filename.endswith(".zip"):
                    zip_file_path = fpath / filename
                    sub_folder = fpath / \
                        os.path.splitext(os.path.basename(filename))[0]
                    if not sub_folder.is_dir():
                        try:
                            with zipfile.ZipFile(zip_file_path, 'r') as zip:
                                zip.extractall(path=sub_folder)

                            # Delete the zip file after extraction
                            os.remove(zip_file_path)

                        # Handle bad zip files
                        except zipfile.BadZipfile as e:
                            print("BAD ZIP: " + str(zip_file_path))
                            try:
                                os.remove(zip_file_path)
                            except OSError as e:
                                if e.errno != errno.ENOENT:
                                    raise

            length_dir = len(os.listdir(fpath))
            message = f"The {self.pdf_type} zip files successfully extracted. The length of directories: {length_dir}"
            return message

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, )
            return f"An error occurred: In line [{exc_tb.tb_lineno}]: {str(e)}"

    def spliting_data(self) -> str:
        fpath = Path(f"{self.curr_path}/data/{self.pdf_type}")

        train_dir = Path(fpath / 'train')
        test_dir = Path(fpath / 'test')

        # Create train_dir if it doesn't exist
        os.makedirs(train_dir, exist_ok=True)

        # Create test_dir if it doesn't exist
        os.makedirs(test_dir, exist_ok=True)

        # Record train and test directory to exclude from removing
        exclude_dir = {train_dir, test_dir}

        try:
            # Create a filtered list of directories to process
            directories_to_process = [folder for folder in os.listdir(
                fpath) if Path(fpath, folder) not in exclude_dir]

            for folder in directories_to_process:
                # Full path to the subfolder
                folder_path = os.path.join(fpath, folder)

                # Listing all the subfolders
                if os.path.isdir(folder_path):
                    files = os.listdir(folder_path)

                    # Split the files into train and test sets
                    train_files = files[:int(len(files) * self.split_ratio)]
                    test_files = files[int(len(files) * self.split_ratio):]

                    # Copy the train files to the train directory
                    for file in train_files:
                        src_file_path = os.path.join(folder_path, file)
                        dst_file_path = os.path.join(train_dir, file)
                        shutil.move(src_file_path, dst_file_path)

                    # Copy the test files to the test directory
                    for file in test_files:
                        src_file_path = os.path.join(folder_path, file)
                        dst_file_path = os.path.join(test_dir, file)
                        shutil.move(src_file_path, dst_file_path)

                # Remove the source folder after splitting
                shutil.rmtree(folder_path)
            return f"Splitting {self.pdf_type} is completed"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, )
            return f"An error occurred: In line [{exc_tb.tb_lineno}]: {str(e)}"

    def get_file_byte_string(self, file) -> bytes:
        curr_file = open(file, "rb")
        data = curr_file.read()
        data_str = str(data)
        data_delim = ' '.join(data_str[i:i+4]
                              for i in range(0, len(data_str), 4))
        data_bytes = bytes(data_delim, 'utf-8')
        curr_file.close()
        return data_bytes

    def create_row(self, filetype, file, writer) -> None:
        file_data = []
        file_data.append(self.id_counter)
        file_data.append(filetype)
        file_data.append(os.path.basename(os.path.normpath(file)))
        bytecode = self.get_file_byte_string(file)
        file_data.append(bytecode)
        writer.writerow(file_data)
        file_data.clear()
        self.id_counter += 1

    def csv_generator(self) -> None:

        fpath = Path(f"{self.curr_path}/data/{self.pdf_type}")

        with open('testing.csv', 'a+') as testing_csv:
            writer = csv.writer(testing_csv)

            writer.writerow(self.header)

            for files in os.listdir(os.path.join(fpath, 'test')):

                # put all this into "do_list_creation(filetype, file) function"
                self.create_row(self.ftype, os.path.join(
                    fpath, 'test', files), writer)

        with open('training.csv', 'a+') as training_csv:
            writer = csv.writer(training_csv)
            writer.writerow(self.header)
            for files in os.listdir(os.path.join(fpath, 'train')):
                self.create_row(self.ftype, os.path.join(
                    fpath, 'train', files), writer)

        return "Succesfully Completed"


def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))

    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message