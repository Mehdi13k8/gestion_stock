@echo off

doskey ok=cd "C:\Users\pc\OneDrive - Epitech\Stage\djangoproject" $T workon "my_env" $T python manage.py runserver
DOSKEY ls=dir
doskey cd=cd %HOMEPATH%
DOSKEY clear=cls
doskey ls=wsl ls --color $*
doskey ll=wsl ls -l --color $*
