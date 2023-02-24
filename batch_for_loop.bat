for /r %%i in (*) do (
    echo %%~ni
    rclone ls --include "*%%~ni*" secret:Documents/Books/ -P
)