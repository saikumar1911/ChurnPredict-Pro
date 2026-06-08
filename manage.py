# File: manage.py



#!/usr/bin/env python
"""Django command-line utility for administrative tasks."""
# Import section
import os
import sys


# Function: main
def main():
    """Run administrative tasks from the command line."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounts.churn_system.settings')
    # Try block
    try:
# Import section
        from django.core.management import execute_from_command_line
    # Except block
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


# If block
if __name__ == '__main__':
    main()
