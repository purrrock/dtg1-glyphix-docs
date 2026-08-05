# Global Resource Migration Guide

This document is intended for Glyphix downstream integration projects, helping you upgrade global resource loading methods from older projects to the latest scheme. This achieves an easily manageable and editable global resource layout without relying on vendor-supplied packaging or conversion tools.

Early versions of Glyphix used `global.pkg` binary archive packages to manage global resources (font files, font mapping tables, etc.). Later, it gradually evolved to directly using unpacked resource files, and finally, the font mapping file format transitioned from binary to standard JSON <version-badge since="0.9" />. If your maintained entry code still uses the old syntax, you can follow this guide to upgrade.

::: tip
Using the old mode introduces maintenance hassles, making it difficult to manage and edit global resources. Upgrading immediately is strongly recommended.
:::

## Removing `global.pkg`

### Old Code Characteristics

If your entry code contains any of the following patterns, it means you are using `global.pkg`:

```cpp
EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
static String globalUri(const String &path) { return "pkg:///" + path; }
```

The effect of these two lines is to route all resource requests with the `pkg:///` protocol to the files inside the `/global.pkg` binary archive package.

Why it needs to be removed:
- Every time fonts or other resources are replaced, the packaging tool must be re-run to generate the `.pkg` file.
- Individual files inside `.pkg` cannot be directly viewed or replaced during debugging, making it difficult to verify contents.
- The packaging process relies on dedicated tools, increasing communication and maintenance costs.

### Migration Steps

**Step 1: Extract resources from `global.pkg`.**

If you no longer have the `.pkg` source files, you can extract the contents from `global.pkg` (using the Glyphix command-line tool or by requesting the original resource files). Typically, you need to extract the following:

```
fonts/
    NotoSans-Regular.ttf
    NotoSansSC-Regular.ttf
    ...
    font-faces          ← Font mapping file (will be upgraded to JSON later)
```

Place the extracted directory into your project's resource directory, for example, `/fonts/`.

**Step 2: Remove `global.pkg` related code.**

1. Delete the entire line `EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg")`.
2. Delete wrapper functions like `globalUri()`.
3. Change all resource references from `pkg:///xxx` to direct file paths, i.e., `/xxx`.

**Step 3: Modify font loading code.**

Assuming your initialization code originally looked like this:

```cpp
static String globalUri(const String &path) { return "pkg:///" + path; }

static void setupFont(const String &fontMap) {
    String uri = globalUri(fontMap);
    FontFaceMap &map = App()->fontManager()->faces();
    if (!map.readFile(uri))
        LogError() << "Failed to load font face map: " << fontMap;
}

int main() {
    Application app;
    EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
    setupFont("font-faces");
    // ...
}
```

Change it to use file paths directly (without the `globalUri()` function and `GlobalPackage` registration):

```cpp
static void setupFont(const String &fontMap) {
    auto &map = App()->fontManager()->faces();
    if (!map.readFile(fontMap))
        LogError() << "Failed to load font face map: " << fontMap;
}

int main() {
    Application app;
    setupFont("/fonts/font-faces");
    // ...
}
```

At this stage, the resource layout becomes:

```
/fonts/
    font-faces          ← Binary format
    NotoSans-Regular.ttf
    ...
```

You are still using the binary `font-faces` file at this stage; the next section will upgrade it to JSON.

## Switching to JSON Font Mapping Files

### Old Code Characteristics

```cpp
FontFaceMap &map = App()->fontManager()->faces();
map.readFile("/fonts/font-faces");
```

`readFile` reads a custom binary format file. This binary file cannot be edited manually and must be converted and generated from CSS files using a packaging tool.

### JSON Format Description

Now, we use a JSON file directly to describe the font mapping relationships. You only need to create a `font-faces.json` file with the following format:

```json
{
  "font-faces": [
    {
      "family": "sans-serif",
      "weight": 400,
      "style": "normal",
      "urls": [
        "NotoSans-Regular.ttf",
        "NotoSansSC-Regular.ttf",
        "NotoSansJP-Regular.ttf"
      ]
    },
    {
      "family": "sans-serif",
      "weight": 700,
      "style": "normal",
      "urls": [
        "NotoSans-Bold.ttf"
      ]
    },
    {
      "family": "serif",
      "weight": 400,
      "style": "normal",
      "urls": [
        "NotoSerif-Regular.ttf"
      ]
    }
  ]
}
```

Field Descriptions:

| Field | Type | Required | Default Value | Description |
|------|------|------|--------|------|
| `family` | String | Yes | - | Font family name, e.g., `sans-serif`, `serif` |
| `weight` | Integer | No | 400 | CSS font weight value (100-900), 400 is regular, 700 is bold |
| `style` | String | No | normal | Font style, options are `italic` or `oblique` |
| `urls` | String Array | Yes | - | Font file paths, relative to the directory where the JSON file is located |

Further explanations for key fields are provided below.

**The `weight` Field**

For `weight`, directly enter the CSS font weight numerical value, which will be rounded to the nearest standard value:

- `100` Thin
- `400` Regular (default value, can be omitted)
- `700` Bold
- `900` Black

**`urls` Path Resolution**

Paths in `urls` are resolved relative to the directory where the JSON file is located. For example, if the JSON file is located at `/fonts/font-faces.json`, writing `"fonts/NotoSans-Regular.ttf"` in `urls` will ultimately be resolved as `/fonts/fonts/NotoSans-Regular.ttf`.

Therefore, it is recommended to place the JSON file directly in the same directory as the font files, allowing URLs to be written simply as file names. For example, the directory layout:

```
/fonts/
    font-faces.json
    NotoSans-Regular.ttf
    NotoSansSC-Regular.ttf
    NotoSans-Bold.ttf
```

The JSON content at this point matches the code snippet above.

### Code Modifications

Replace `readFile` in the initialization code with `readJSON`:

```cpp
#include "gx_fontmanager.h"

static void setupFont() {
    auto &map = App()->fontManager()->faces();
    if (!map.readJSON("/fonts/font-faces.json"))
        LogError() << "Failed to load font-faces.json";
    App()->setFont(Font("sans-serif", 24));
}

int main() {
    Application app;
    setupFont();
    // ...
}
```

Only this single API call needs to be changed; no other code needs to be modified. Afterwards, you can directly edit `font-faces.json` to add/remove fonts or adjust mapping relationships without needing any conversion tools.

## FAQ

**How to handle multiple variants (Regular, Bold, Italic, etc.) for the same family?**

Add an independent entry for each variant in the `font-faces` array, distinguishing them using `weight` and `style`:

```json
{
  "font-faces": [
    {
      "family": "sans-serif",
      "weight": 400,
      "style": "normal",
      "urls": ["NotoSans-Regular.ttf"]
    },
    {
      "family": "sans-serif",
      "weight": 700,
      "style": "normal",
      "urls": ["NotoSans-Bold.ttf"]
    },
    {
      "family": "sans-serif",
      "weight": 400,
      "style": "italic",
      "urls": ["NotoSans-Italic.ttf"]
    }
  ]
}
```

MCU projects typically only use the Regular `sans-serif` font with `normal` weight, and the system will automatically fall back.

**Can multiple files be placed in the `urls` array? When is it needed?**

Yes. When a font family needs to cover multi-language characters, put multiple font files into the same `urls` array. For example, if `sans-serif` needs to support Latin letters, CJK characters, and Arabic simultaneously:

```json
{
  "family": "sans-serif",
  "weight": 400,
  "style": "normal",
  "urls": [
    "NotoSans-Regular.ttf",
    "NotoSansSC-Regular.ttf",
    "NotoSansJP-Regular.ttf",
    "NotoSansArabic.ttf"
  ]
}
```

When rendering text, the engine will search for character glyphs in these files sequentially, and the first matched glyph will be used.

**Must the font files and JSON be in the same directory?**

No. Paths in `urls` are resolved relative to the JSON file's directory; you can use relative paths to place fonts in subdirectories. Absolute paths can also be used, in which case they are unaffected by the JSON directory.

**Can a JSON string be passed directly in code?**

Yes. Use the two-parameter overloaded version:

```cpp
map.readJSON("/fonts/", R"({
  "font-faces": [
    {"family": "sans-serif", "urls": ["NotoSans-Regular.ttf"]}
  ]
})");
```

The first parameter is `baseUri`, used to resolve relative paths in `urls`.