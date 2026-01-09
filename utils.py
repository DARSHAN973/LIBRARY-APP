"""
Utility functions for the library app
"""
import webbrowser
import subprocess
import sys


def open_url_safely(url):
    """
    Safely open URL in browser with fallbacks for different platforms.
    Works on Android, iOS, Linux, Windows, and macOS.
    
    Args:
        url (str): The URL to open
        
    Returns:
        bool: True if URL was opened successfully, False otherwise
    """
    try:
        # Check if running on Android
        try:
            from android.runnable import run_on_ui_thread
            from jnius import autoclass, cast
            
            def open_url_android():
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                
                intent = Intent()
                intent.setAction(Intent.ACTION_VIEW)
                intent.setData(Uri.parse(url))
                currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
                currentActivity.startActivity(intent)
            
            run_on_ui_thread(open_url_android)()
            return True
        except ImportError:
            # Not on Android, continue to other methods
            pass
        
        # Check if running on iOS
        try:
            from pyobjus import autoclass
            NSURL = autoclass('NSURL')
            UIApplication = autoclass('UIApplication')
            
            url_obj = NSURL.URLWithString_(url)
            UIApplication.sharedApplication().openURL_(url_obj)
            return True
        except ImportError:
            # Not on iOS, continue to other methods
            pass
        
        # Desktop platforms
        if sys.platform == 'linux':
            # Try xdg-open first (most Linux distributions)
            try:
                subprocess.Popen(['xdg-open', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            except (FileNotFoundError, Exception):
                pass
        
        # Try standard webbrowser for all platforms
        webbrowser.open(url)
        return True
        
    except Exception as e:
        print(f"Error opening URL: {e}")
        # Last resort fallback for Linux
        if sys.platform == 'linux':
            try:
                for browser in ['firefox', 'google-chrome', 'chromium', 'chromium-browser']:
                    try:
                        subprocess.Popen([browser, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        return True
                    except FileNotFoundError:
                        continue
            except Exception:
                pass
        return False
