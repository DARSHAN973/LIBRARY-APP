"""
Utility functions for the library app
"""
import webbrowser
import subprocess
import sys
import threading
from kivy.utils import platform as kivy_platform
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.label import MDLabel


_ACTIVE_ANDROID_DIALOGS = []


class LoadingOverlay:
    """Delayed loading overlay that appears only for longer operations."""

    def __init__(self, message="Loading...", delay=0.5):
        self.message = message
        self.delay = delay
        self._show_event = None
        self._visible = False
        self._modal = None

    def start(self):
        self.stop()
        self._show_event = Clock.schedule_once(self._show, self.delay)

    def _show(self, _dt):
        self._show_event = None

        # Outer card (shadow layer)
        shadow = BoxLayout(
            size_hint=(None, None),
            size=(dp(196), dp(168)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
        with shadow.canvas.before:
            Color(0, 0, 0, 0.18)
            shadow.shadow_bg = RoundedRectangle(
                size=shadow.size,
                pos=(shadow.x + dp(3), shadow.y - dp(3)),
                radius=[dp(20)],
            )
        shadow.bind(
            pos=lambda inst, v: setattr(inst.shadow_bg, 'pos', (inst.x + dp(3), inst.y - dp(3))),
        )

        # Inner card
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=[dp(24), dp(22), dp(24), dp(20)],
            size_hint=(None, None),
            size=(dp(192), dp(164)),
        )
        with content.canvas.before:
            Color(1, 1, 1, 1)
            content.bg = RoundedRectangle(
                size=content.size,
                pos=content.pos,
                radius=[dp(20)],
            )
        content.bind(
            size=lambda inst, v: setattr(inst.bg, 'size', inst.size),
            pos=lambda inst, v: setattr(inst.bg, 'pos', inst.pos),
        )

        spinner_box = FloatLayout(size_hint_y=None, height=dp(60))
        spinner_box.add_widget(
            MDSpinner(
                size_hint=(None, None),
                size=(dp(48), dp(48)),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                active=True,
                color=(0.13, 0.59, 0.95, 1),
            )
        )
        content.add_widget(spinner_box)

        content.add_widget(
            MDLabel(
                text=self.message,
                halign='center',
                bold=True,
                theme_text_color='Custom',
                text_color=(0.15, 0.15, 0.15, 1),
                size_hint_y=None,
                height=dp(30),
            )
        )

        self._modal = ModalView(
            size_hint=(1, 1),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.5),
            auto_dismiss=False,
        )
        center_wrap = FloatLayout()
        shadow.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        content.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        center_wrap.add_widget(shadow)
        center_wrap.add_widget(content)
        self._modal.add_widget(center_wrap)
        self._modal.open()
        self._visible = True

    def stop(self):
        if self._show_event is not None:
            self._show_event.cancel()
            self._show_event = None
        if self._visible and self._modal is not None:
            self._modal.dismiss()
        self._modal = None
        self._visible = False


def run_with_loading(
    _widget,
    worker,
    on_success,
    on_error=None,
    message="Loading...",
    delay=0.5,
):
    """Run worker in background thread and show delayed loading overlay."""
    loader = LoadingOverlay(message=message, delay=delay)
    loader.start()

    def background_task():
        try:
            result = worker()

            def done(_dt):
                loader.stop()
                on_success(result)

            Clock.schedule_once(done, 0)
        except Exception as exc:

            def fail(_dt):
                loader.stop()
                if on_error:
                    on_error(exc)

            Clock.schedule_once(fail, 0)

    threading.Thread(target=background_task, daemon=True).start()


def open_url_in_app_webview(url, title="Reader"):
    """Open a URL inside the Android app using a native WebView dialog.

    Returns True when in-app opening is triggered successfully.
    Returns False on non-Android platforms or when Android WebView fails.
    """
    if kivy_platform != 'android':
        return False

    try:
        from jnius import autoclass, cast

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Dialog = autoclass('android.app.Dialog')
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')

        activity = cast('android.app.Activity', PythonActivity.mActivity)
        dialog = Dialog(activity)
        dialog.setTitle(title)

        webview = WebView(activity)
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setBuiltInZoomControls(True)
        settings.setDisplayZoomControls(False)
        settings.setLoadWithOverviewMode(True)
        settings.setUseWideViewPort(True)

        # Keep all navigation inside this WebView.
        webview.setWebViewClient(WebViewClient())
        webview.loadUrl(url)

        dialog.setContentView(
            webview,
            LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT),
        )
        dialog.show()

        # Keep a reference while open so it is not collected unexpectedly.
        _ACTIVE_ANDROID_DIALOGS.append(dialog)
        return True
    except Exception as e:
        print(f"Error opening in-app webview: {e}")
        return False


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
        if kivy_platform == 'android':
            from jnius import autoclass, cast

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')

            intent = Intent()
            intent.setAction(Intent.ACTION_VIEW)
            intent.setData(Uri.parse(url))
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            currentActivity.startActivity(intent)
            return True
        
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
