## Setup the SDK

    sudo apt-get install p7zip-full
    sudo wget  https://www.waveshare.net/w/upload/8/80/IT8951_20200319_Release.7z
    7z x IT8951_20200319_Release.7z -O./IT8951

## Put fiels in this repository to overwrite corresponding files in IT8951 directory
## Compile epd.so library

    cd IT8951/
    sudo make clean
    sudo make

