from django.db import models
from datetime import datetime
from django.utils import timezone
import pyodbc
import os
from django.contrib.auth import get_user_model  # Correto

User = get_user_model()


   
