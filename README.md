# 🎷 Music Transcriber

A Python tool that turns video screenshots of sheet music into clean, organized PDF pages using Python + OpenCV + PIL. Automates screenshotting, filters out duplicates, extracts music areas, and generates printable sheets. Many videos on Youtube have sheet music transcription, however the transcriptions are fragmented over different intervals of the video making it difficult to use when one wants to play the music with an instrument at their own pace. These videos typically have a PDF transcription, but are generally behind a paywall. Subsequently, this tool aims to provide free jazz music to those who want to play for personal pleasure. 

## 🔧 Setup

1. Clone the repo:
git clone git@github.com:conradcreates/music_reconstructor.git
cd music_reconstructor

2. Run the setup script:
chmod +x setup_music_env.sh
./setup_music_env.sh

## Usage

1. Run the screenshotter.
    - This captures screen images every few seconds and saves only then saves unique ones into a seperate directory using OpenCV to detect similarity.
    - python3 screenshotter.py <interval_in_seconds> <start_delay_in_seconds>
    - python3 screenshotter.py 2 5
    - This waits 5 seconds, then takes a screenshot every 2 seconds until you stop it (Ctrl+C). It then filters duplicates and triggers the music processor.

2. Process screenshots
- music_processor.py is automatically called after the screenshots are done. It crops out the music sections using OpenCV and saves them to screenshots/processed/.
- Manual running is also possible with python3 music_processor.py

3. Build the PDF
- Once images are processed and correct run: python3 construct_pages.py <output_folder_name>
- Eg. python3 construct_pages.py autumn_leaves
- This will arrange processed music fragments into pages and save a PDF

# Output folders
- screenshots/ → Raw captures
- screenshots/unique/ → Filtered non-duplicates
- screenshots/processed/ → Cropped music areas
- <music_name>/pdf_pages/ → Final pages + music_sheet.pdf

# Tips
- Run in full screen for best screenshot quality.
- Check first/last images are correct before generating the PDF.
