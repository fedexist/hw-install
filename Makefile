init:
  pip install -r requirements.txt
  python setup.py install
  chmod 755 ./helpers/askpass.sh
  chmod 755 ./helpers/ssh_copy_id_script.sh