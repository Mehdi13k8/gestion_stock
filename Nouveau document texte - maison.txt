@echo off

doskey ok=cd "C:\Users\dieti\OneDrivev1\Documents\gestion_stock\djangoproject" $T workon "my_env" $T python manage.py runserver 0.0.0.0:80
DOSKEY ls=dir
DOSKEY cd=cd %HOMEPATH%
DOSKEY clear=cls
doskey ls=wsl ls --color $*
doskey ll=wsl ls -l --color $*
