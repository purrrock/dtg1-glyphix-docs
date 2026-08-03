---
icon: help-circle-outline
---
# Frequently Asked Questions

## Bundling Tools

### Project Build Issues

#### `Lisp Error: thread killed` Error

Specifically, an error message similar to the following appears:

``` log
[ 47%] Process image src/assets/images/frame1.png
error: Lisp Error: thread killed
```

This issue is caused by an error in a preceding build task, which causes the ongoing image conversion build task to be canceled. Simply fix the build task that threw the `fatal` error to resolve it; no special handling is required for this error itself.

### Emulator

#### Default Emulator Language

The default language for the emulator is `zh-CN`. Therefore, if you have added [i18n](/framework/component/i18n.md) configurations, the `zh-CN.json` translation file will be used by default. When running the emulator with the `gx` command, you can use the `-l` or `--language` option to specify the language:
``` shell
gx emu -l en-US # Use American English
```
You can also dynamically change the language using the inspector debugging tool while the emulator is running.