---
icon: image-filter
---
# Image management

The glyphix.js packaging tool will manage all PNG image resources in the project (`src` directory). Related modules mainly provide the following functions:
- Supports configuration files for image resources and provides related configuration interfaces
- Convert images to device-optimized sizes and formats when packaging

Application developers only need to configure the packaging parameters of image resources according to their own needs, while device vendors need to define specific image conversion strategies for devices.

## Application development configuration

In application development, you need to configure image packaging parameters to correctly generate resource packages.
Configuring `config/image-rules.json` and `config.designWidth` of `src/menifest.json` during application development will affect the packaging behavior of image resources. `config/image-rules.json` is generally used to configure quality and performance parameters, while the fields in `menifest.json` affect the global scaling of the image (used to adapt to devices with different resolutions).

::: tip
`config/image-rules.json` can be configured using the `gx config` command or other methods, but it is not recommended to edit it directly with a text editor.
:::

If using the `gx config` command, developers will mainly focus on two parameters: transparent and quality.

### Transparent parameter

Transparent indicates whether the image contains transparent pixels. If it is configured as no (`false`) and the resource image contains transparent pixels, these pixels will be converted to opaque when generated (usually superimposed on a black background). Therefore, necessary images need to be marked as preserving transparent pixels, otherwise incorrect overlay effects will be displayed. Since opaque images perform better on some platforms and require less data, the transparent option is turned off by default.

### Quality parameters

The Quality parameter represents the quality of the packaged image and is an integer in the range of $[0, 100]$. However, generally only 3 rough quality levels are used:
- High: 100, indicating the highest quality
- Middle: 50, medium quality, default value
- Low: 0, low quality

When converting image resources, they will be optimized according to quality parameters. Generally speaking, medium quality is a conversion strategy that balances factors such as display effect, drawing/loading performance, and memory resource usage on the target platform, so it is recommended. Using high quality may have better quality, but may incur performance degradation. Low quality can be used for images where quality can be lost to improve performance (such as photos). Specific target platforms may also ignore the quality parameter and use a unified strategy.

## Device and platform adaptation

Assuming that device and platform developers have implemented optimized image resource formats for specific target platforms and support multiple qualities and pixel formats, the following work needs to be done in order to generate these image formats in glyphix.js:
- Command line tools required to achieve **single image** conversion
  - Must provide a command line interface for converting PNG images to custom formats, supporting output to a specified path (including overwriting the original file)
  - It is best to provide a command line interface for converting from a custom format to a PNG image, and support output to a specified path (including overwriting the original file). Without this function, PC break preview will not be possible.
- Write device description files and image conversion scripts

### Image conversion script

The image conversion script is a scheme file. When an image needs to be converted, glyphix.js will call this script. The latter can determine how to convert the image based on these variables:
- `env.image-path`: The absolute path of the image to be converted, the converted image is overwritten and written to this path
- `env.transparent`: the transparency parameter of this image
- `env.quailty`: the quality parameters of this image
- `env.target`: Convert target mode, see description below
- `env.verbose`: Whether to enable verbose mode, if so, detailed logs can be output, otherwise logs should not be output
- `env.script-dir`: The absolute path where the current script file is located. If the command required for conversion is relative to this script file and not in the `PATH` environment variable, you can use this parameter for splicing

`env.target` represents the **target mode** of image conversion, and its value determines which conversion method is applied:
- `"device"`: performs a complete conversion process for the target device, such as removing the transparent channel of the opaque image, and then converting it to PGF format (Glyphix picture format) according to the quality parameters
- `"emulator"`: Execute the conversion process for the simulator. Since the simulator does not support the texture format of specific hardware (such as ETC2, etc.), in order to ensure that the image is displayed normally in the simulator, you can only remove the transparent channel of the opaque image without further conversion to the target device format (or convert to the PGF format supported by the software)
- `"preprocess"`: Only perform the preprocessing step, that is, remove the transparent channel of the opaque image, and output the result in PNG format
- `"preview"`: To generate a PNG image for preview, you must first convert the image into a custom target format according to the conversion process of the `"device"` target, and then convert the output image back to PNG for preview use

::: tip
If the command line tool for image conversion does not support converting a custom format to PNG, then do not implement the `"preprocess"` and `"preview"` target modes.
:::

### image-forge command line tool

image-forge is a PGF image format command line tool provided by Glyphix and has the following functions:
- Supports converting PNG images to PGF format, and converting PGF to PNG images
- Supports common ARGB and PAL pixel formats, and distinguishes premultiplied alpha modes
- Supports blending transparent ARGB images onto a specified solid color background to convert them into opaque images (instead of directly discarding the alpha channel)
- Supports line alignment by pixels or bytes
- Supports LZ4 compression and can set the minimum compression threshold (image data below the threshold will not be compressed)

For platforms using other custom image formats, image-forge can also be used to remove the transparency channel.

## Image conversion script example

The following example demonstrates how to use commands such as image-forge to convert PNG to PGF images, using the color lookup table (PAL) format first.

First define the target format in the opaque and transparent cases:
``` scheme
; Define pixel format rules for opaque colors
(define (opaque-formats q)
  (cond ((<= q 50) "pal-rgb")
        (else "rgb24")))

; Define pixel format rules for transparent colors
(define (transparent-formats q)
  (cond ((<= q 50) "pal-argb-premul")
        (else "argb32-premul")))

; Calculate target pixel format under transparency and quality parameters
(define pixel-format
  ((if env.transparent
      transparent-formats opaque-formats)
    env.quailty))

; Whether the image is converted to color lookup table format
(define palette (<= env.quailty 50))
```

The above code will use the color lookup table format when the quality is 50 or less, and will use `pal-rgb` or `pal-argb` depending on whether it is transparent or not. Quality above 50 uses RGB or ARGB 8bit sampled pixel format. Finally, the `pixel-format` variable is the name of the actual pixel format used, and `palette` indicates whether to use the color lookup table format.

Next define the commands that need to be used in various situations:

``` scheme
; Whether to add the --verbose command line parameter
(define if-verbose (if env.verbose "--verbose " ""))

; Call the pngquant command to reduce the image color to less than 256 colors. pngquant needs to be installed in the system.
(define color-reduction
  (string-append "pngquant --ext=.png --force " if-verbose env.image-path))

; Convert image to PGF format
(define convert (string-append "image-forge "
  "--format=" pixel-format " " ; Specify the output pixel format
  "--compress --min-compress-ratio=5 " ; Compress image data to reduce file size, the minimum compression ratio is 5
  "--align=16 --pixel-align " ; Align the image to 16 pixels
  if-verbose
  env.image-path))

; Remove image alpha channel and add background
(define remove-alpha (string-append "image-forge --bypass "
  ; On bes2500ibp watches, non-transparent images can have their alpha channel removed and blended with a black background, which improves image quality after PAL color reduction
  (if env.transparent "" "--background black ")
  if-verbose
  env.image-path))

; Command to convert PGF image back to PNG
(define decode
  (string-append "image-forge --decode " if-verbose env.image-path))
```

In the following code, `execute-try` calls the specified `f` function after the command exits with a non-zero value. The `execute` function prints an error log and exits the script abnormally after the command exits with a non-zero value. The `run-convert` function performs the complete target device image conversion process (calling the `remove-alpha` and `convert` commands).

``` scheme
; Execute a command and print the command content in verbose mode, calling function f if the command exits with a non-zero exception
(define (execute-try cmd f)
  (begin
    (if env.verbose; If it is verbose mode, print the command content
      (display (string-append "Run command: " cmd "\n")))
    (let ((r (system (string-append env.script-dir "/bin/" cmd))))
      (if (= r 0) 0 (f r)))
  ))

; Execute a command and print the command content in verbose mode. If the command exits abnormally, the program will exit.
(define (execute cmd)
  (execute-try cmd (lambda (x)
    (begin; print error code and exit abnormally when failure occurs
      (display (string-append "subprocess failed (" (number->string x) "): " cmd "\n"))
      (exit-fail)
  ))))

;Convert image
(define (run-convert)
  (begin
    (execute remove-alpha) ; Remove the transparent channel first
    (if palette (execute color-reduction)) ; If it is a color lookup table format, reduce the number of pixels in the image
    (execute convert) ; Execute image conversion command
  ))
```

The `targets` macro defines the processing methods for all target modes. For example, the `"device"` mode will call the `run-convert` function, etc.

``` scheme
; Define the conversion strategy corresponding to the target
(targets env.target
  ; Device mode: the final image conversion process for the target device
  ("device" (run-convert))
  ; Simulator mode: only remove the alpha channel of non-transparent images, without converting the format
  ("emulator" (execute remove-alpha))
  ; Preprocessing mode: remove the alpha channel of non-transparent images and add a background
  ("preprocess" (execute remove-alpha))
  ; Preview mode: generate a PNG preview image that is consistent with the display effect of the actual device
  ("preview" (begin
    (run-convert) ; First convert the image to PGF format
    (execute decode))) ; Convert the image back to PNG
  )
```

### Use image conversion script

To use the image conversion script, you need to add a field to the device model description file:

```yaml
description: default watch

screen:
  width: 454 # pixels
  height: 454 #pixels
  dpi: 326 # pixels per inch

# ...
image-build: image-convert-pal.scm # The path of the image conversion script relative to this Yaml file
```

### More complex strategies

Since the image conversion script is a complete programming language rather than configuration languages ​​such as Yaml and JSON, we can implement more complex custom conversion strategies without being limited by the functions provided by the framework. Take the above color lookup table format conversion as an example: PAL format does not work well on pictures with rich colors. At this time, the picture can be converted to a format that performs better in such scenes. The specific ideas are:
1. The `pngquant` command supports exiting abnormally if the quality after conversion to PAL format is lower than the specified value, so configure the command parameters according to this purpose
2. In the `run-convert` function, the `color-reduction` operation performed by `execute` is changed to be performed by `execute-try`, and the alternative format conversion operation is used in the latter's exception handling function.
3. Targets such as `preview` are processed in a similar manner, but please note that when converting the output format to PNG, you also need to recognize that the command exits abnormally and continue trying with subsequent commands.

All in all, it is similar to the idea of ​​​​a shell script, using the abnormal exit code of the command to control the process.