"""
PDF Viewer for Kivy Mobile App
Opens PDF files in WebView or native Android PDF viewer
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
import os
import requests
from pathlib import Path


class PDFViewer:
    """Handle PDF viewing for mobile application"""
    
    PDF_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".library_app_cache")
    
    @staticmethod
    def ensure_cache_dir():
        """Create cache directory if it doesn't exist"""
        os.makedirs(PDFViewer.PDF_CACHE_DIR, exist_ok=True)
    
    @staticmethod
    def get_cached_pdf_path(pdf_url):
        """Get local path for cached PDF"""
        PDFViewer.ensure_cache_dir()
        
        # Create a filename from URL hash
        filename = f"{hash(pdf_url)}.pdf"
        return os.path.join(PDFViewer.PDF_CACHE_DIR, filename)
    
    @staticmethod
    def download_pdf(pdf_url, local_path):
        """Download PDF from URL and save locally"""
        try:
            response = requests.get(pdf_url, timeout=30)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception as e:
            print(f"Error downloading PDF: {e}")
        return False
    
    @staticmethod
    def open_pdf_android(pdf_url):
        """Open PDF in Android native viewer"""
        try:
            jnius_mod = __import__('jnius', fromlist=['autoclass'])
            autoclass = jnius_mod.autoclass
            
            # Get the PDF file
            local_path = PDFViewer.get_cached_pdf_path(pdf_url)
            
            # Download if not cached
            if not os.path.exists(local_path):
                if not PDFViewer.download_pdf(pdf_url, local_path):
                    return False
            
            # Use Android Intent to open PDF
            PythonJavaClass = autoclass('org.kivy.android.PythonActivity')
            activity = PythonJavaClass.mActivity
            
            File = autoclass('java.io.File')
            Uri = autoclass('android.net.Uri')
            Intent = autoclass('android.content.Intent')
            FileProvider = autoclass('androidx.core.content.FileProvider')
            
            file = File(local_path)
            uri = FileProvider.getUriForFile(
                activity,
                'org.example.libraryapp.fileprovider',
                file
            )
            
            intent = Intent()
            intent.setAction(Intent.ACTION_VIEW)
            intent.setDataAndType(uri, 'application/pdf')
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            
            activity.startActivity(intent)
            return True
        except Exception as e:
            print(f"Error opening PDF with Android: {e}")
            return False
    
    @staticmethod
    def open_pdf_webview(pdf_url, parent_widget=None):
        """Open PDF in WebView (fallback for desktop testing)"""
        try:
            webview_mod = __import__('kivy.uix.webview', fromlist=['WebView'])
            WebView = webview_mod.WebView
            
            local_path = PDFViewer.get_cached_pdf_path(pdf_url)
            
            # Download if not cached
            if not os.path.exists(local_path):
                if not PDFViewer.download_pdf(pdf_url, local_path):
                    print("Failed to download PDF")
                    return False
            
            # Create WebView with PDF
            layout = FloatLayout()
            
            # Create a simple HTML file that embeds the PDF
            html_path = local_path.replace('.pdf', '.html')
            html_content = f"""
            <html>
                <head>
                    <title>PDF Viewer</title>
                    <style>
                        body {{ margin: 0; padding: 0; }}
                        #pdf-container {{ width: 100%; height: 100vh; }}
                    </style>
                </head>
                <body>
                    <embed id="pdf-container" src="file://{local_path}" type="application/pdf" />
                </body>
            </html>
            """
            
            with open(html_path, 'w') as f:
                f.write(html_content)
            
            webview = WebView(url=f'file://{html_path}')
            layout.add_widget(webview)
            
            popup = Popup(title='PDF Viewer', content=layout, size_hint=(1, 1))
            popup.open()
            return True
        except Exception as e:
            print(f"Error opening PDF with WebView: {e}")
            return False
    
    @staticmethod
    def open_pdf(pdf_url):
        """
        Open PDF - tries Android native first, falls back to WebView
        
        Args:
            pdf_url: URL of the PDF to open
        """
        from kivy.core.window import Window
        
        # Try Android native first
        if PDFViewer.open_pdf_android(pdf_url):
            return True
        
        # Fallback to WebView
        return PDFViewer.open_pdf_webview(pdf_url)


def open_book_reader(parent_instance, pdf_link, book_title):
    """
    Convenience function to open a book PDF
    
    Args:
        parent_instance: Parent widget
        pdf_link: PDF URL
        book_title: Title of the book
    """
    if PDFViewer.open_pdf(pdf_link):
        print(f"Opening: {book_title}")
    else:
        print(f"Failed to open PDF: {pdf_link}")
