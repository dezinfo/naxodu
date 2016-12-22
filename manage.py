#!/usr/bin/env python
import os
import sys
# import django.core.management.commands.runserver as runserver
if __name__ == "__main__":
    # runserver.DEFAULT_PORT="8001"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "naxodu.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
