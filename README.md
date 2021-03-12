# Download-Kit
Download-kit is an extensible multi-protocol download kit with multiple file download protocols like http,ftp etc.

**Currently Supported Protocols:**
* http
* https
* ftp
* sftp

## Usage

### Install 
 1. The Installation requires Python>=3.7 
 2. Install requirements.txt
 3. Install the download_kit package using `setup.py`
```
cd download_kit
pip3 install requirements.txt
python3 setup.py install
```

### Input Urls File 
An input file containing urls in each line sample in `inputfile.txt` file are from 
http://speedtest.ftp.otenet.gr/
The input file needs to be passed as runtime parameter with `-i` or `--inputFile` option.

Ftp & sftp might require username and password which can be passed in the url as shown in the sample below
`sftp://user:password@sample.com/somedir/somefile.txt`
    Here we are downloading `somefile.txt` from `sample.com` giving `username = user` and `password = password`.
     

### Output Directory Setup 
The output directory need to be defined with `-o` or `--output_dir` option with directory name.if directory doesn't exist setup will try to create one during runtime.

### Run Download Kit
Run following command after installing download-kit using above [Install](#Install) to run the sample Url's in `inputfile.txt` 
```
download_kit -o download -i inputfile.txt
```
in other words  download_kit -o <[output Directory](#output-directory-setup)> -i <[inputfile](#input-urls-file)>

## Test Download Kit

To test the download kit run `pytest`
```
cd download_kit
pytest
```
This should give result as shown below :
![Pytest output](images/pytest.png?raw=true "test output")


## Resultant Downloads

Once the run is successful the result on the cli should look like the image below :

![Download_kit output](images/output.png?raw=true "download output")


