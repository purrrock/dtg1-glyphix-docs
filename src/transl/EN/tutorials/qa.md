---
icon: help-circle-outline
---
# Frequently Asked Questions

## Packaging Tools

### Project Build Issues

#### `Lisp Error: thread killed` Error

The specific symptom is an error message similar to the following:

``` log
[ 47%] Process image src/assets/images/frame1.png
error: Lisp Error: thread killed
```

This issue occurs because a previous build step failed, causing the ongoing image conversion build operation to be cancelled. You only need to fix the build operation with the `fatal` error to recover; no special handling is required.

### Simulator

#### Simulator Default Language

The default language of the simulator is `zh-CN`. Therefore, if you have added [internationalization](/framework/component/i18n.md) configuration, it will default to using the `zh-CN.json` translation file. You can use the `-l` or `--language` option with the `gx` command to specify the language when running the simulator:
``` shell
gx emu -l en-US # Use American English
```
You can also dynamically change the language while the simulator is running using the inspector debugging tool.