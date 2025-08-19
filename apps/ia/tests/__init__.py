# Tests package
import sys
import os

# Ajouter le répertoire parent au PATH pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .test_activities import *
from .test_registrations import *