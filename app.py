import datetime as dt
# from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

##### DATABASE setup#####
engine = create_engine('sqlite:///hawaii.sqlite', connect_args={'check_same_thread': False})
# reflecting it to new model
Base = automap_base()
# reflect the tables
