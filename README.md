# GoogleImageScraping

GoogleImageScraping is a tool that automatically downloads Google images in original resolution

## Demo

![demo](https://github.com/shotaxx00/GoogleImageScraping/wiki/images/demo.gif)

## Features

- Download Google image in original resolution automatically
- Save as JPG image

## Requirement

- Python 3.x
- Chome Driver (Download same version of Google Chrome you are using)
  - [ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/)

## Installation

```
git clone https://github.com/shotaxx00/GoogleImageScraping.git
```

## Usage

```
python GoogleImageScraping.py -k [keyword] -n [number] -p [path]
```

- keyword : A keyword for search Google image
- number : Number of download
- path : Path to save image

#### Example(Demo)

```
python GoogleImageScraping.py -k dog -n 30 -p ./download
```

## Auther

[@shotaxx00](https://github.com/shotaxx00/)

## License

[MTI](https://opensource.org/licenses/MIT)
