from platform import system
import os


def get_de():
    desktop_env = os.environ.get("XDG_CURRENT_DESKTOP").lower()
    if not desktop_env:
        desktop_env = os.environ.get("DESKTOP_SESSION").lower()
    if "kde" in desktop_env or "plasma" in desktop_env:
        return "kde"
    elif "gnome" in desktop_env:
        return "gnome"
    elif "xfce" in desktop_env:
        return "xfce"
    elif "lxde" in desktop_env:
        return "lxde"
    elif "cinnamon" in desktop_env:
        return "cinnamon"
    elif "mate" in desktop_env:
        return "mate"
    elif "unity" in desktop_env:
        return "unity"
    else:
        return "unknown"


if system() == "Windows":
    import ctypes

    def change_wallpaper(uri):
        uri = uri.replace("/", "\\")
        ctypes.windll.user32.SystemParametersInfoA(20, 26, uri, 1)

elif system() == "Darwin":
    from os import system as s

    def change_wallpaper(uri):
        s(
            'osascript -e \'tell application "Finder" to set desktop picture to POSIX file "{0}"\''.format(
                uri
            )
        )

elif system() == "Linux":
    import subprocess
    from os import system as s

    def get_output(command):
        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        out, err = p.communicate()
        return out

    try:
        de = get_de()
        if de == "gnome":
            v = int(get_output("gnome-session --version").split()[-1][0])
            if v == 2:

                def change_wallpaper(uri):
                    subprocess.run(
                        [
                            "gconftool-2",
                            "--type=string",
                            -"-set",
                            "/desktop/gnome/background/picture_filename",
                            uri,
                        ]
                    )

            elif v == 3:

                def change_wallpaper(uri):
                    subprocess.run(
                        [
                            "gsettings",
                            "set",
                            "org.gnome.desktop.background",
                            "picture-uri" f'"file://{uri}"',
                        ]
                    )

        if de == "kde":

            def change_wallpaper(uri):
                subprocess.run(["plasma-apply-wallpaperimage", uri], check=True)

    except:
        raise OSError("Wallaper Change is supported in GNOME 2/3 and Unity only")
