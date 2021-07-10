import os

version_dir = '../alembic/versions'
next_index = len(os.listdir(version_dir))
next_revision_id = str(next_index).zfill(4)
#print('alembic revision --autogenerate --rev-id ' + next_revision_id)

os.chdir('../')
os.system('alembic revision --autogenerate --rev-id ' + next_revision_id)
os.system('alembic upgrade head')
