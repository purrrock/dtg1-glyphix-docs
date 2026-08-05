---
icon: image-filter
---
# Image Management

The glyphix.js packaging tool manages all PNG image resources in the project (`src` directory). The related modules mainly provide the following features:
- Supports configuration files for image resources and provides a related configuration interface
- Converts images into device-optimized sizes and formats during packaging

Application developers only need to configure the packaging parameters for image resources according to their needs, while device vendors need to define specific image conversion strategies for their devices.

## Application Development Configuration

In application development, image packaging parameters must be configured to correctly generate resource packages.
Configuring `config/image-rules.json` and properties such as `config.designWidth` in `src/manifest.json` during application development will affect the packaging behavior of image resources. `config/image-rules.json` is generally used to configure quality and performance parameters, while fields in `manifest.json` affect the global scaling ratio of images (used to adapt to devices of different resolutions).

::: tip
`config/image-rules.json` can be configured using the `gx config` command or other methods, but direct editing with a text editor is not recommended.
:::

If using the `gx config` command, developers will primarily focus on two parameters: `transparent` and `quality`.

### Transparent Parameter

The `transparent` parameter indicates whether the image contains transparent pixels. If configured as `false` while the source image does contain transparent pixels, these pixels will be converted to opaque (usually blended onto a black background) during generation. Therefore, necessary images must be marked to preserve transparent pixels; otherwise, incorrect overlay effects will be displayed. Because opaque images have better performance on certain platforms and consume less data, the `transparent` option is disabled by default.

### Quality Parameter

The `quality` parameter represents the quality of the packed image, which is an integer in the range $[0, 100]$. However, typically only 3 approximate quality levels are used:
- High: 100, indicating the highest quality
- Middle: 50, medium quality, the default value
- Low: 0, low quality

Image resources are optimized based on the quality parameter during conversion. Generally speaking, medium quality is a conversion strategy that balances display quality, rendering/loading performance, and memory resource consumption on the target platform, and is therefore recommended. Using high quality may provide better visual fidelity, but could result in degraded performance. Low quality can be used for images where quality can be sacrificed to improve performance (such as photographs). Specific target platforms may also ignore the `quality` parameter and use a unified strategy instead.

## Device and Platform Adaptation

Assuming device and platform developers have implemented optimized image resource formats for specific target platforms supporting multiple quality and pixel formats, the following work is required to generate these image formats within glyphix.js:
- Implement a command-line tool required for **single image** conversion
  - Must provide a command-line interface to convert from PNG images to a custom format, supporting output to a specified path (including overwriting the original file)
  - Preferably provide a command-line interface to convert from a custom format back to PNG images, supporting output to a specified path (including overwriting the original file). Without this feature, PC-side previews will not be available
- Write device description files and image conversion scripts

### Image Conversion Script

The image conversion script is a Scheme file. When an image needs to be converted, glyphix.js invokes this script, which uses the following variables to determine how to convert the image:
- `env.image-path`: The absolute path of the image to be converted; the converted image overwrites this path.
- `env.transparent`: The transparency parameter of this image.
- `env.quailty`: The quality parameter of this image.
- `env.target`: The conversion target mode, described later.
- `env.verbose`: Whether verbose mode is enabled. If true, detailed logs can be output; otherwise, no logs should be output.
- `env.script-dir`: The absolute path of the current script file. If the command required for conversion is relative to this script file rather than in the `PATH` environment variable, this parameter can be used for concatenation.

`env.target` represents the **target mode** for image conversion, and its value determines the specific conversion method applied:
- `"device"`: Executes the complete conversion process targeting the target device, such as removing the alpha channel of opaque images and then converting them into the PGF format (Glyphix Image Format) according to the quality parameter.
- `"emulator"`: Executes the conversion process targeting the emulator. Since the emulator does not support specific hardware texture formats (such as ETC2, etc.), to ensure images display correctly in the emulator, only the alpha channel of opaque images may be removed without further conversion to the target device format (or converted to a software-supported PGF format).
- `"preprocess"`: Executes only the preprocessing steps, which means removing the alpha channel of opaque images and outputting the result in PNG format.
- `"preview"`: Generates a preview PNG image. First, convert the image to the custom target format following the `"device"` target conversion process, and then convert the output image back to PNG for preview purposes.

::: tip
If the command-line tool for image conversion does not support converting custom formats to PNG, do not implement the `"preprocess"` and `"preview"` target modes.
:::

### image-forge Command-Line Tool

`image-forge` is the PGF image format command-line tool provided by Glyphix, featuring the following capabilities:
- Supports converting PNG images to PGF format, as well as PGF to PNG images.
- Supports common ARGB and PAL pixel formats, distinguishing between premultiplied alpha modes.
- Supports blending transparent ARGB images onto a specified solid color background to convert them into opaque images (rather than directly discarding the alpha channel).
- Supports row alignment by pixels or bytes.
- Supports LZ4 compression, with the ability to set a minimum compression threshold (image data below the threshold will not be compressed).

Platforms using other custom image formats can also utilize `image-forge` to remove the alpha channel.

## Image Conversion Script Example

The following example demonstrates how to use commands like `image-forge` to convert PNGs to PGF images, prioritizing the palette (PAL) format.

First, define the target formats for opaque and transparent conditions:
``` scheme
; Define pixel format rules for opaque colors
(define (opaque-formats q)
  (cond ((<= q 50) "pal-rgb")
        (else "rgb24")))

; Define pixel format rules for transparent colors
(define (transparent-formats q)
  (cond ((<= q 50) "pal-argb-premul")
        (else "argb32-premul")))

; Calculate the target pixel format under the influence of transparency and quality parameters
(define pixel-format
  ((if env.transparent
      transparent-formats opaque-formats)
    env.quailty))

; Whether the image is converted to a palette format
(define palette (<= env.quailty 50))
```

The above code uses the palette format when the quality is less than or equal to 50, using `pal-rgb` or `pal-argb` depending on transparency. For qualities higher than 50, it uses 8-bit per channel RGB or ARGB pixel formats. Ultimately, the `pixel-format` variable represents the actual pixel format name used, and `palette` indicates whether the palette format is used.

Next, define the commands needed for various scenarios:

``` scheme
; Whether to add the --verbose command-line argument
(define if-verbose (if env.verbose "--verbose " ""))

; Call the pngquant command to reduce image colors to 256 or fewer; pngquant must be installed on the system
(define color-reduction
  (string-append "pngquant --ext=.png --force " if-verbose env.image-path))

; Convert image to PGF format
(define convert (string-append "image-forge "
  "--format=" pixel-format " " ; Specify output pixel format
  "--compress --min-compress-ratio=5 " ; Compress image data to reduce file size, minimum compression ratio is 5
  "--align=16 --pixel-align " ; Align image to 16 pixels
  if-verbose
  env.image-path))

; Remove image Alpha channel and add background
(define remove-alpha (string-append "image-forge --bypass "
  ; On the bes2500ibp watch, non-transparent images can have their alpha channel removed and blended with a black background; this operation improves image quality after PAL color reduction
  (if env.transparent "" "--background black ")
  if-verbose
  env.image-path))

; Command to decode PGF image back to PNG
(define decode
  (string-append "image-forge --decode " if-verbose env.image-path))
```

In the code below, `execute-try` calls a specified `f` function when a command exits with a non-zero status, while the `execute` function prints an error log and exits the script with an exception when a command exits with a non-zero status. The `run-convert` function executes the complete target device image conversion workflow (calling `remove-alpha` and `convert` commands).

``` scheme
; Execute a command and print command contents in verbose mode; if the command exits with a non-zero exception, call function f
(define (execute-try cmd f)
  (begin
    (if env.verbose ; Print command contents if in verbose mode
      (display (string-append "Run command: " cmd "\n")))
    (let ((r (system (string-append env.script-dir "/bin/" cmd))))
      (if (= r 0) 0 (f r)))
  ))

; Execute a command, print command contents in verbose mode, and exit the program if the command exits with an exception
(define (execute cmd)
  (execute-try cmd (lambda (x)
    (begin ; Print error code and exit exceptionally upon failure
      (display (string-append "subprocess failed (" (number->string x) "): " cmd "\n"))
      (exit-fail)
  ))))

; Convert image
(define (run-convert)
  (begin
    (execute remove-alpha) ; Remove transparency channel first
    (if palette (execute color-reduction)) ; Reduce image pixel count if palette format is used
    (execute convert) ; Execute image conversion command
  ))
```

The `targets` macro defines the processing methods for all target modes, such as the `"device"` mode calling the `run-convert` function, etc.

``` scheme
; Define conversion strategies corresponding to targets
(targets env.target
  ; Device mode: Image conversion workflow ultimately used for the target device
  ("device" (run-convert))
  ; Emulator mode: Only remove the alpha channel of non-transparent images, do not convert format
  ("emulator" (execute remove-alpha))
  ; Preprocess mode: Remove the alpha channel of non-transparent images and add background
  ("preprocess" (execute remove-alpha))
  ; Preview mode: Generate a PNG preview image consistent with the actual device display effect
  ("preview" (begin
    (run-convert) ; Convert image to PGF format first
    (decode))) ; Then convert image back to PNG
  )
```

### Using the Image Conversion Script

To use the image conversion script, add a field to the device model description file:

``` yaml
description: default watch

screen:
  width: 454 # pixels
  height: 454 # pixels
  dpi: 326 # pixels per inch

#...
image-build: image-convert-pal.scm # Path of the image conversion script relative to this Yaml file
```

### More Complex Strategies

Since the image conversion script is a full programming language rather than a configuration language like Yaml or JSON, we can implement more complex custom conversion strategies without being limited by the features provided by the framework. Taking the aforementioned palette format conversion as an example: the PAL format performs poorly on color-rich images. In such cases, images can be converted to a format that performs better in these scenarios. The general approach is as follows:
1. The `pngquant` command supports exiting with an exception when the quality falls below a specified value after PAL format conversion; configure command parameters accordingly for this purpose.
2. Modify the `color-reduction` operation executed by `execute` in the `run-convert` function to be executed by `execute-try` instead, using an alternative format conversion operation in the latter's exception handling function.
3. The handling for targets like `preview` is similar, but note that when converting the output format back to PNG, command exit exceptions must also be detected and handled by subsequent fallback commands.

In summary, following a shell-script-like approach, you use the exit codes of commands to control the workflow.