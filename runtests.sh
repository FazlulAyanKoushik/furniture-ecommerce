# /bin/bash

python3 projectile/manage.py test core.rest.tests
python3 projectile/manage.py test accountio.rest.tests
python3 projectile/manage.py test catalogio.rest.tests
python3 projectile/manage.py test gruppio.rest.tests
python3 projectile/manage.py test weapi.rest.tests