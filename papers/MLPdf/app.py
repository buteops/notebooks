#!/usr/bin/env python3

from __future__ import annotations
import os, logging, time
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
from io import BytesIO, StringIO
from enum import Enum
from uuid import UUID

import streamlit as st
import pandas as pd
from pandas import DataFrame, Series

from utils import PDFMalicious, DataTransformations

# Page Config
st.set_page_config(
   page_title="Home ● tf-facial-pdf-security",
   page_icon="💻",
   layout="wide",
   initial_sidebar_state="expanded",
)


def send_interations_data(id: UUID, initial_date: str, files_name: str) -> str:
   """Will send generated data from user interactions to database"""
   ...


if __name__ == '__main__':
   transform = DataTransformations(pdf_type='benign', ftype=24)
   print(transform.curr_path)
   print(os.path.join(os.getcwd(), 'datasets'))