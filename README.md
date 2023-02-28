# ValidDataSet

<a id="menu"></a>

* [About](#about)
* [Plugins](#plugins)
* [Installation](#installation)
* [Usage](#usage)

## <a id="about"></a>About    <font size="1">[ [Menu](#menu) ]</font>

`ValidDataSet` was created to help validate datasets created based on the Lj Speech Dataset (for Tacotron, Flowtron, Waveglow, or RadTTS).

`VDS` works based on plugins (which can be dynamically added by the user in the future).

Descriptions of current plugins can be found in the [Plugins](#plugins) section.


## <a id="plugins"></a>Plugins    <font size="1">[ [Menu](#menu) ]</font>

Below is a list of currently used plugins (new ones will be added over time).

|  ID  | Name                                | Version | Description                                                               |
| --- | --- | --- | --- |
| F001 | WavsTranscriptionChecker            | 23.2.26 | Check if all files have been added to the transcription files             |
| T001 | DatasetStructureChecker             | 23.2.26 | Check if the "wavs" folder and transcription files exist in the dataset   |
| T002 | EmptyLineChecker                    | 23.2.26 | Check if there are empty lines in the transcriptions                      |
| T003 | FilesInTranscriptionChecker         | 23.2.26 | Check if all files added to transcription exist                           |
| T004 | ExistingWavFileTranscriptionChecker | 23.2.26 | Check if all files added to transcription have a transcription            |
| T005 | PunctuationMarksChecker             | 23.2.26 | Check if all transcriptions end with punctuation marks: ".", "?" or "!"   |
| T006 | PunctuationMarksChecker             | 23.2.26 | Check if all lines have the same number of PIPE characters                |
| T007 | DuplicatedTranscriptionChecker      | 23.2.26 | Check if there are any duplicate paths to WAV files in the transcriptions |

## <a id="installation"></a>Installation    <font size="1">[ [Menu](#menu) ]</font>

To install ValidDataSet, use the following command:

```shell
pip install vds
```

## <a id="usage"></a>Usage    <font size="1">[ [Menu](#menu) ]</font>

List of parameters supported by VDS:

```text
 -p, --path            Path to dataset
 -d, --disable         Disable plugins
 -f, --files           Set transcription file names
     --list-plugins    List plugins
 -v, --verbose         Print additional information
```

Sample commands and their description:

List all plugins:
```shell
vds --list-plugins
```

Run `VDS` with all plugins without additional information:
```shell
vds --path /media/username/Disk/Dataset_name/
```

Run `VDS` with all plugins with additional information:
```shell
vds --path /media/username/Disk/Dataset_name/ -v
```

Run `VDS` without plugins F001,T002,T006 with additional information:
```shell
vds --path /media/username/Disk/Dataset_name/ --disable F001,T002,T006 -v
```

Run `VDS` without plugins F001,T002,T006 with own transcription names and with additional information:
```shell
vds --path /media/username/Disk/Dataset_name/ --disable F001,T002,T006 --files train.txt,val.txt -v
```
