@echo off

doskey ok=cd "C:\Users\pc\OneDrive - Epitech\Stage\gestion_stock\djangoproject" $T workon "env_gest_stock" $T python manage.py runserver
DOSKEY ls=dir
DOSKEY cd=cd %HOMEPATH%
DOSKEY clear=cls
doskey ls=wsl ls --color $*
doskey ll=wsl ls -l --color $*
