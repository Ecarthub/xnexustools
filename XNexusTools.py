import sys
from PIL import Image
import pytesseract
import os
import cv2
from scipy import ndimage
from skimage import filters
import speech_recognition as sr
import yt_dlp

# Set Tesseract executable path for Linux
pytesseract.pytesseract.tesseract_cmd_linux = '/usr/bin/tesseract'
# Set Tesseract executable path for Windows
pytesseract.pytesseract.tesseract_cmd_windows = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Determine the operating system and set Tesseract executable accordingly
if sys.platform.startswith('win'):
    pytesseract.pytesseract.tesseract_cmd = pytesseract.pytesseract.tesseract_cmd_windows
else:
    pytesseract.pytesseract.tesseract_cmd = pytesseract.pytesseract.tesseract_cmd_linux


def close_windows():
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def voice_to_text():
    # Function to perform speech-to-text conversion and append the transcribed text to a file
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)
        print("Recognizing...")

        try:
            text = recognizer.recognize_google(audio_data)
            print("Transcribed: ", text)
            print()

            with open("transcribed_text.txt", "a") as text_file:
                text_file.write("transcribed: " + text + "\n")
                print('The transcribed text are stored in image_to_text.txt')

        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        finally:
            if 'text' in locals():
                print("Transcribed text appended to transcribed_text.txt")
            else:
                print("Failed to transcribe audio")
            sys.exit()


def extract_text_from_image(image_path):
    with Image.open(image_path) as img:
        extracted_text = pytesseract.image_to_string(img)
        return extracted_text


def option_1():
    print("You are in Image text convert to text")
    print("Note: Must the image text are readable for better results.")
    print()
    while True:
        imgpath = input("Please enter the image path (press Enter for default): ")

        if imgpath == '':
            imgpath = 'default_image.jpg'  # Default image path
            break
        elif os.path.exists(imgpath):
            break
        else:
            print("Error: Can't find the", imgpath,
                  "|Please recheck the path file and try again. If the file is in the same directory, just put the file and its extension (e.g., example.jpeg)|")

    # Path to the image file
    image_path = imgpath

    # Extract text from the image
    try:
        texts = extract_text_from_image(image_path)

        # Print the extracted text
        print(texts)

        # Write the extracted text to a file
        with open("image_to_text.txt", "a") as text_file:
            text_file.write("transcribed: " + texts + "\n")

        # Print a message indicating that the text has been stored in image_to_text.txt
        print("The extracted text has been stored in image_to_text.txt.")

    except Exception as e:
        print("An error occurred while processing the image:", e)

    # Add a loop to return to the main menu
    while True:
        choice = input("Do you want to process another image? (yes/no): ").lower()
        if choice == 'yes':
            break
        elif choice == 'no':
            return  # Exit the function
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")


def option_2():
    print("You selected Option 2")
    while True:
        imgpath = input("Please enter the image path (press Enter for default): ")

        if imgpath == '':
            imgpath = 'default_image.jpg'  # Default image path
            break
        elif os.path.exists(imgpath):
            print()
            print("1. Grayscale")
            print("2. Sobel Edges")
            print("3. Gaussian Blur")
            print("4. Median Filtered")
            print()

            choice = input("Please enter what kind of filter you want: ")

            if choice == '1':
                print()
                print("Note: Press any letter in your keyboard to exit.")
                print()
                image = cv2.imread(imgpath)
                grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cv2.imshow('Grayscale Image', grayscale_image)
                close_windows()  # Properly close OpenCV windows
                break

            elif choice == '2':
                print()
                print("Note: Press any letter in your keyboard to exit.")
                print()
                image = cv2.imread(imgpath)
                grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                sobel_edges = filters.sobel(grayscale_image)
                cv2.imshow('Sobel Edges', sobel_edges)
                close_windows()  # Properly close OpenCV windows
                break

            elif choice == '3':
                print()
                print("Note: Press any letter in your keyboard to exit.")
                print()
                image = cv2.imread(imgpath)
                gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)
                cv2.imshow('Gaussian Blur', gaussian_blur)
                close_windows()  # Properly close OpenCV windows
                break

            elif choice == '4':
                print()
                print("Note: Press any letter in your keyboard to exit.")
                print()
                image = cv2.imread(imgpath)
                median_filtered = cv2.medianBlur(image, 5)
                cv2.imshow('Median Filtered', median_filtered)
                close_windows()  # Properly close OpenCV windows
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 4.")
        else:
            print("Error: Can't find the", imgpath, "|Please recheck the path file and try it again. If the file is in the same directory, just put the image name and its extension (e.g., example.jpeg)| Ctrl+c to cancel")


def option_3():
    voice_to_text()


def option_4():
    # Download the video
    vidurl = input('Enter the URL of the YouTube video: ')
    quality = input('Input the quality you desire (e.g., 1080 or 2160): ')
    output_path = input('Enter the full path where you want to save the video: ')

    # Create a yt_dlp.YoutubeDL object with options for the desired video quality and MP4 format
    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best',
        'outtmpl': output_path + '/%(title)s.%(ext)s',  # Output file name template with title and extension
        'merge_output_format': 'mp4',    # Merge video and audio streams into MP4 format
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([vidurl])


def main_menu():
    print("XNexus Tools")
    print("1. Image convert to text")
    print("2. Apply Advanced Filters")
    print("3. Voice Convert to text")
    print('4. Youtube Downloader')
    print("5. Exit")


# Main program loop
while True:
    main_menu()
    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        option_1()
    elif choice == '2':
        option_2()
    elif choice == '3':
        option_3()
    elif choice == '4':
        option_4()
    elif choice == '5':
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 5.")
