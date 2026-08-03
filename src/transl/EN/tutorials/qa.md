---
icon: help-circle-outline
---
# FAQ

## Packaging tools

### Project build issues

#### `Lisp Error: thread killed` error report

The specific phenomenon is that an error message similar to the following appears:

``` log
[ 47%] Process image src/assets/images/frame1.png
error: Lisp Error: thread killed
```

This problem is due to a previous build error, which caused the image conversion build operation being executed to be cancelled. You only need to fix the `fatal` error reporting build operation to resume without special processing.

### Emulator

#### Simulator default language

The default language of the simulator is `zh-CN`. Therefore, if you add the [Internationalization](/framework/component/i18n.md) configuration, the `zh-CN.json` translation file will be used by default. To run the simulator with the `gx` command you can use the `-l` or `--language` option to specify the language:
``` shell
gx emu -l en-US # Use American English
```
You can also change the language dynamically while the emulator is running using the inspector debugging tool.
