# fig_to_mp4
Convert multiple images into a single MP4 file

## Requirement
```shell
pip install opencv-python
pip3 install pytk
```

## Getting Started
1. Run `fig_to_mp4.py`.
2. Select the directory where the image files are located.
3. You can either select another directory or cancel to start the processing.

#### 3.1. Command Line Execution
```shell
python fig_to_mp4.py
```

#### 3.2. Script Execution
Script files (`exe.bat` and `exe.ps1`) are provided for Windows users.
- `exe.bat`: Double-click `exe.bat`
- `exe.ps1`: Right-click `exe.ps1` and select `Run with PowerShell`.

> [!NOTE]
> It's always welcome to add script files for Mac or Linux.
> Please make one and open a pull request.

#### 3.3. Config
`"output_video": 0` ; The movie will be exported to the source directory.

`"output_video": 1` ; The movie will be exported to the image directory.

## Contributing
Any bug fixes or feature enhancements are welcome! To contribute, first [open an issue](https://opensource.guide/how-to-contribute/#opening-an-issue), then [open a pull request](https://opensource.guide/how-to-contribute/#opening-an-issue).
