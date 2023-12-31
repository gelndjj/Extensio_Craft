<a name="readme-top"></a>

[![Contributors][contributors-shield]](https://github.com/gelndjj/Active_Directory_Automate/graphs/contributors)
[![Forks][forks-shield]](https://github.com/gelndjj/Active_Directory_Automate/forks)
[![Stargazers][stars-shield]](https://github.com/gelndjj/Active_Directory_Automate/stargazers)
[![Issues][issues-shield]](https://github.com/gelndjj/Active_Directory_Automate/issues)
[![MIT License][license-shield]](https://github.com/gelndjj/Active_Directory_Automate/blob/main/LICENSE)
[![LinkedIn][linkedin-shield]](https://www.linkedin.com/in/jonathanduthil/)


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/gelndjj/Extensio_Craft">
    <img src="https://github.com/gelndjj/Extensio_Craft/blob/main/resources/icon.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Extensio Craft</h3>

  <p align="center">
    A Python application for streamlined file extension management.
    <br />
    <a href="https://github.com/gelndjj/Extensio_Craft"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/gelndjj/Extensio_Craft/issues">Report Bug</a>
    ·
    <a href="https://github.com/gelndjj/Extensio_Craft/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>

  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
<div align="center">
ExtensioCraft is a Python-based application designed to facilitate file system operations with an emphasis on managing file extensions. This tool leverages both command-line and graphical user interface elements, making it versatile and user-friendly.</br>
<img src="https://github.com/gelndjj/Extensio_Craft/blob/main/resources/app_mac.png" alt="Screenshot" width="812" height="590">
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

# Usage 

Use ExtensioCraft to manage file extensions efficiently. You can browse directories, select specific file types, and perform various file operations.

### Comboboxes
#### Folder Combobox: 
- This dropdown menu displays a list of previously browsed directories. Users can select a directory from this list to quickly navigate to it. It's updated every time a new folder is browsed and saved.
### Listboxes
#### Extension Listbox: 
- Shows all file extensions found in the currently selected directory. Each entry in this listbox represents a unique file extension present in the directory. Users can select one or more extensions to perform operations like copying or deleting files with these extensions.
#### Path Listbox:
- Displays the paths of the files or directories related to the selected file extensions from the Extension Listbox. It helps users see where files with the selected extensions are located within the chosen directory.
### Buttons

#### Browse Button:
- Opens a dialog for the user to select a directory. Once a directory is selected, the application scans it for file extensions and updates the Extension Listbox with these extensions.
#### Refresh Button:
- Refreshes the application, particularly useful for updating the Extension Listbox if there are changes in the selected directory or if a new directory is selected from the Folder Combobox.
#### Browse Specific Button:
- Allows users to enter a specific file extension and filter the Extension Listbox to show only files with that extension.
#### Delete Selected Extensions Button:
- Deletes all files in the selected directories (from the Path Listbox) that have extensions selected in the Extension Listbox.
##### Copy Selected Extensions Button:
- Copies all files in the selected directories that have the chosen extensions to a specified destination folder. The destination folder is chosen by the user.
#### Go to Folder Button:
- Opens the file explorer (Finder on macOS, Explorer on Windows, etc.) and navigates to the selected folder or file location from the Path Listbox.
#### Checkboxes (Filter Options)
- Pictures, Videos, Document Files, Compression Files, Software Files, Others Checkboxes: These are filter options. Selecting any of these checkboxes filters the extensions shown in the Extension Listbox based on the category chosen. For example, selecting "Pictures" will filter and display only image file extensions like .jpg, .png, etc.
#### Additional Functionalities
- Progress Bar: Indicates the progress of ongoing operations like scanning directories, copying, or deleting files. It provides visual feedback to the user on the task's progress.
- Saving and Loading Paths: The application saves the paths of browsed directories and loads them when restarted, providing ease of access to frequently used locations.

## Screenshots (MacOS)
<div align="center">
<img src="https://github.com/gelndjj/Extensio_Craft/blob/main/resources/screen1.png" alt="Screenshot" width="406" height="295">
<img src="https://github.com/gelndjj/Extensio_Craft/blob/main/resources/screen2.png" alt="Screenshot" width="406" height="295">
</div>


<!-- GETTING STARTED -->
## Standalone APP (MacOS)

1. Install pyintaller
```
pip install pyinstaller
```
2. Generate the standalone app
```
pyinstaller --windowed --onefile your_script_name.py
```
- --windowed or -w flag is used to prevent the Terminal from opening. 
- --onefile creates a single executable file.

3. After the process completes, find your executable in the dist directory.
</br>
4. Create a Folder for Your App: Name it YourAppName.app and ensure it ends with .app. Inside this folder, create a hierarchy like this:
</br>

```
YourAppName.app/
└── Contents/
    ├── MacOS/
    └── Resources/
```

5. Move Your Executable: Move the PyInstaller-generated executable into the Contents/MacOS/ directory. Rename it to match your application's name.
</br>
6. Create an Info.plist File: In the Contents/ directory, create a file named Info.plist with the following basic structure:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>YourAppName</string>
    <key>CFBundleIconFile</key>
    <string>iconfile</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.yourapp</string>
    <key>CFBundleName</key>
    <string>YourAppName</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>NSHighResolutionCapable</key>
    <string>True</string>
</dict>
</plist>

```

7. Replace YourAppName and other details with your app's specifics.
Add an Icon: Optionally, add your app's icon to the Resources folder and reference it in the Info.plist.

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".


1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built With

<a href="https://www.python.org">
<img src="https://github.com/gelndjj/Extensio_Craft/blob/main/resources/py_icon.png" alt="Icon" width="32" height="32">
</a>
&nbsp
<a href="https://customtkinter.tomschimansky.com">
</a>
<p align="right">(<a href="#readme-top">back to top</a>)</p>
    

<!-- LICENSE -->
## License

Distributed under the GNU GENERAL PUBLIC LICENSE. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact


[LinkedIn](https://www.linkedin.com/in/jonathanduthil/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
