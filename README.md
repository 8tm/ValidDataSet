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

| ID   | Name                                | Version | Description                                                                                  |
|------|-------------------------------------|---------|----------------------------------------------------------------------------------------------|
| F001 | WavsTranscriptionChecker            | 23.3.9  | Check if all files have been added to the transcription files                                |
| F002 | WavPropertiesChecker                | 23.3.9  | Check if all files are mono, 22050 Hz with length between 2 and 10 seconds                   |
| F003 | WavCorrectnessChecker               | 23.4.2  | Check if all wav files will not throw WavFileWarning on load or they don't have other errors |
| T001 | DatasetStructureChecker             | 23.3.9  | Check if the "wavs" folder and transcription files exist in the dataset                      |
| T002 | EmptyLineChecker                    | 23.3.9  | Check if there are empty lines in the transcriptions                                         |
| T003 | FilesInTranscriptionChecker         | 23.3.9  | Check if all files added to transcription exist                                              |
| T004 | ExistingWavFileTranscriptionChecker | 23.3.9  | Check if all files added to transcription have a transcription                               |
| T005 | PunctuationMarksChecker             | 23.3.9  | Check if all transcriptions end with punctuation marks: ".", "?" or "!"                      |
| T006 | PunctuationMarksChecker             | 23.3.9  | Check if all lines have the same number of PIPE characters                                   |
| T007 | DuplicatedTranscriptionChecker      | 23.3.9  | Check if there are any duplicate paths to WAV files in the transcriptions                    |

## <a id="installation"></a>Installation    <font size="1">[ [Menu](#menu) ]</font>

To install ValidDataSet, use the following command:

```shell
pip install vds
```

## <a id="usage"></a>Usage    <font size="1">[ [Menu](#menu) ]</font>

Command in Linux: vds or vds-win

Command in Windows: vds-win

List of parameters supported by VDS:

```text
 -v, --verbose                    Print additional information
 -o, --output                     Save output to file

     --plugins.list               List plugins
     --plugins.disable            List of plugins to disable like: F001,T002,T006

     --args.path                  Path to dataset
     --args.files                 Set transcription file names like: train.txt,val.txt
     --args.dir-name              wavs folder name (default: wavs)
     --args.sample-rate           Set sample rate (default: 22050)
     --args.number-of-channels    Set number of channels (default: 1 [mono])
     --args.min-duration          Set minimum duration in miliseconds (1000 ms = 1 second)
     --args.max-duration          Set maximum duration in miliseconds (1000 ms = 1 second)
     --args.number-of-pipes       Set number of pipes (|) (default: 1)
```

Sample commands and their description:

List all plugins:
```shell
vds --plugins.list
```

Run `VDS` with all plugins without additional information:
```shell
vds --args.path /media/username/Disk/Dataset_name/
```

Run `VDS` with all plugins with additional information:
```shell
vds --args.path /media/username/Disk/Dataset_name/ -v
```

Run `VDS` without plugins F001,T002,T006 with additional information:
```shell
vds --args.path /media/username/Disk/Dataset_name/ --plugins.disable F001,T002,T006 -v
```

Run `VDS` without plugins F001,T002,T006 with own transcription names and with additional information:
```shell
vds --args.path /media/username/Disk/Dataset_name/ --plugins.disable F001,T002,T006 --args.files train.txt,val.txt -v
```

Run `VDS` and print files which are longer than 20 seconds, shorter than 2 seconds and not in mono:
```shell
vds --args.path /media/username/Disk/Dataset_name/ --args.min-duration 2000 --args.max-duration 20000 --args.number-of-channels 2 -v
```
