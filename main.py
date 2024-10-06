import customtkinter as ctk
import yt_dlp
import threading
import os
import subprocess

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Youtube Downloader")
        self.iconbitmap("C:\\Program Files (x86)\\YoutubeDownloader\\icon.ico")
        self.minsize(width=550,height=400)
        self.maxsize(width=550,height=400)
        self.configure(padx=20,pady=20)

        self.youtube_downloader_folder = os.path.expanduser("~\\Desktop\\Youtube Downloader")
        self.ffmpeg_path = os.path.join(os.getcwd(), 'ffmpeg.exe') # You need ffmpeg.exe 

        self.text_font = ('Arial', 18, 'normal')
        self.info_font = ('Arial',20,'bold')
        self.error_font = ('Arial',9,'normal')

        self.file_name = None
        self.audio_url = None
        self.video_url = None
        self.file_path = None

        self.file_name_label = ctk.CTkLabel(self,text="Enter file name : ",font=self.text_font)
        self.file_name_label.place(relx=0, rely=0)
        self.file_name_entry = ctk.CTkEntry(self,width=360)
        self.file_name_entry.place(relx=0.3,rely=0)


        self.link_label = ctk.CTkLabel(self, text="Enter file link    : ", font=self.text_font)
        self.link_label.place(relx=0, rely=0.15)
        self.link_entry = ctk.CTkEntry(self,width=360)
        self.link_entry.place(relx=0.3,rely=0.15)

        self.download_mp3_button = ctk.CTkButton(self,text="Download Mp3",font=self.text_font,command=self.start_download_mp3)
        self.download_mp3_button.place(relx=0.35,rely=0.33,anchor=ctk.CENTER)

        self.download_mp4_button = ctk.CTkButton(self, text="Download Mp4", font=self.text_font,command=self.start_download_mp4)
        self.download_mp4_button.place(relx=0.65, rely=0.33,anchor=ctk.CENTER)

        self.info_label = ctk.CTkLabel(self,font=self.info_font)

        self.show_path = ctk.CTkLabel(self,font=self.text_font)
        self.error_label = ctk.CTkLabel(self,font=self.error_font)

        self.open_file_in_folder_button = ctk.CTkButton(self,text="Open file in folder",font=self.text_font,command=self.open_file_in_folder)

        self.github_link = ctk.CTkLabel(self,text="github.com/mustafaicer")
        self.github_link.place(relx=0.5,rely=0.99,anchor=ctk.CENTER)

    def finally_work(self):
        self.info_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.file_name_entry.delete(0, ctk.END)
        self.link_entry.delete(0, ctk.END)

    def download_mp3(self):
        self.audio_url = self.link_entry.get()
        self.file_name = self.file_name_entry.get()

        try:
            ydl_options = {
                'format': 'bestaudio/best',
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }
                ],
                'outtmpl': f'{self.youtube_downloader_folder}/{self.file_name}'
            }

            with yt_dlp.YoutubeDL(ydl_options) as ydl:
                ydl.download([self.audio_url])

            self.file_path = f"{self.youtube_downloader_folder}\\{self.file_name}.mp3"
            self.info_label.configure(text="Success",text_color="light blue")
            self.show_path.configure(text=f"{self.file_path}")
            if self.error_label is not None:
                self.error_label.configure(text="")
            self.show_path.place(relx=0.5,rely=0.6,anchor=ctk.CENTER)
            self.open_file_in_folder_button.place(relx=0.5,rely=0.75,anchor=ctk.CENTER)

        except Exception as e:
            if self.show_path is not None:
                self.show_path.configure(text="")
            self.info_label.configure(text="ERROR",text_color="red")
            self.error_label.configure(text=f"{e}")
            self.error_label.place(relx=0.5,rely=0.6,anchor=ctk.CENTER)
        finally:
            self.finally_work()

    def start_download_mp3(self):
        thread = threading.Thread(target=self.download_mp3)

        self.info_label.configure(text="Wait", text_color="light blue")
        self.info_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        thread.start()

    def download_mp4(self):
        self.video_url = self.link_entry.get()
        self.file_name = self.file_name_entry.get()

        try:
            ydl_options = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': os.path.join(self.youtube_downloader_folder, f"{self.file_name}"),
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }]
            }
            with yt_dlp.YoutubeDL(ydl_options) as ydl:
                ydl.download(self.video_url)
            self.file_path = f"{self.youtube_downloader_folder}\\{self.file_name}.mp4"
            self.info_label.configure(text=f"Success",text_color="light blue")
            self.open_file_in_folder_button.place(relx=0.5,rely=0.65,anchor=ctk.CENTER)
            self.show_path.configure(text=f"{self.file_path}")
            if self.error_label is not None:
                self.error_label.configure(text="")
            self.show_path.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
            self.open_file_in_folder_button.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)
        except Exception as e:
            if self.show_path is not None:
                self.show_path.configure(text="")
            self.info_label.configure(text=f"ERROR", text_color="red")
            self.error_label.configure(text=f"{e}")
            self.error_label.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        finally:
            self.finally_work()

    def start_download_mp4(self):
        thread = threading.Thread(target=self.download_mp4)

        self.info_label.configure(text="Wait", text_color="light blue")
        self.info_label.place(relx=0.5, rely=0.50, anchor=ctk.CENTER)

        thread.start()

    def open_file_in_folder(self):
        subprocess.run(["explorer", "/select,", self.file_path])

if __name__ == "__main__":
    window = App()
    window.mainloop()