#!/bin/bash

# Start the first process - run makemigrations
python3 manage.py makemigrations
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start migrate: $status"
  exit $status
fi

# Start the second process - run migrate
python3 manage.py migrate
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start migrate: $status"
  exit $status
fi

# Start the third process - run migrate with syncdb
python3 manage.py migrate --run-syncdb
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start migrate: $status"
  exit $status
fi

#If update file not present, then skip creating users
if [ -f /grabwack/newsetup ]; then
  # Start the fourth process - create admin user
  python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"
  status=$?
  if [ $status -ne 0 ]; then
    echo "Failed to create admin user: $status"
    exit $status
  fi
fi


# Start the fifth process - run server
python3 manage.py runserver 0.0.0.0:8000
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start server or listen on 8000: $status"
  exit $status
fi
