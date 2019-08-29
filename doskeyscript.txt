@echo off

doskey ok=z: $T cd "Z:\GESTION DE STOCK\gestion_stock\djangoproject" $T workon "env_gest_stock" $T python manage.py runserver 0.0.0.0:80 
DOSKEY ls=dir
DOSKEY cd=cd %HOMEPATH%
DOSKEY clear=cls
doskey ls=wsl ls --color $*
doskey ll=wsl ls -l --color $*
