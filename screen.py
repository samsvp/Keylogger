import sys


platform = sys.platform

if platform in ["Windows", "win32", "cywin"]:
    from typing import Optional
    from ctypes import wintypes, windll, create_unicode_buffer

    # https://stackoverflow.com/questions/10266281/obtain-active-window-using-python

    def get_active_window_title() -> Optional[str]:
        hWnd = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(hWnd)
        buf = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hWnd, buf, length + 1)

        return buf.value if buf.value else None

elif platform in ["linux", "linux2"]:
    import subprocess
    
    def get_active_window_title():
        get_window = "xprop -id $(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2) _NET_WM_NAME | cut -d '=' -f 2 | cut -b 1-2 --complement | rev | cut -c 2- | rev 2>&1"
        window = subprocess.check_output(["/bin/bash", "-c", get_window], stderr=subprocess.DEVNULL).decode('UTF-8').rstrip()
        return window if window else "Terminal"