# Global Resource Migration Guide

This document is intended for downstream Glyphix integration projects, helping you upgrade global resource loading methods from legacy projects to the latest scheme. This provides an easily manageable and editable global resource layout, eliminating the dependency on vendor packaging or conversion tools.

In the early days, Glyphix used the `global.pkg` binary archive package to manage global resources (font files, font mapping tables, etc.). Later, it gradually evolved to directly use unpackaged resource files, and finally, the format of the font mapping file was transitioned from binary to standard JSON <version-badge since="0.9" />. If the entry code you maintain still uses the old syntax, you can follow this article to upgrade.

::: tip
Using the old mode brings maintenance hassles and difficulties in managing and editing global resources. It is strongly recommended to upgrade immediately.
:::

## Removing `global.pkg`

### Characteristics of Old Code

If your entry code contains either of the following patterns, it means you are using `global.pkg`:

```cpp
EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg");
static String globalUri(const String &path) { return "pkg:///" + path; }
```

The effect of these two lines is to route all resource requests with the `pkg:///` protocol to files inside the `/global.pkg` binary archive package.

Why it needs to be removed:
- Every time fonts or other resources are changed, the packaging tool must be re-run to generate the `.pkg` file.
- Individual files inside `.pkg` cannot be directly viewed or replaced during debugging, making content verification difficult.
- The packaging workflow depends on dedicated tools, increasing communication and maintenance costs.

### Migration Steps

**Step 1: Extract resources from `global.pkg`.**

If you no longer have the source `.pkg` file, you can extract the contents from `global.pkg` (using the Glyphix command-line tool or by requesting the original resource files). Typically, you need to extract the following:

```
fonts/
    NotoSans-Regular.ttf
    NotoSansSC-Regular.ttf
    ...
    font-faces          ← Font mapping file (will be upgraded to JSON later)
```

Place the extracted directory into your project's resource directory, for example, `/fonts/`.

**Step 2: Remove code related to `global.pkg`.**

1. Delete the entire line `EnvPath::setEntry(EnvPath::GlobalPackage, "/global.pkg")`.
2. Delete wrapper functions like `globalUri()`.
3. Change all resource references of `pkg:///xxx` to direct file paths, i.e., `/xxx`.

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

Change it to use direct file paths (without the `globalUri()` function and `GlobalPackage` registration):

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

At this phase, you are still using the binary `font-faces` file. The next section upgrades it to JSON.

## Switching to JSON Font Mapping Files

### Characteristics of Old Code

```cpp
FontFaceMap &map = App()->fontManager()->faces();
map.readFile("/fonts/font-faces");
```

`readFile` reads a custom binary format file. This binary file cannot be edited manually and must be converted and generated from a CSS file using a packaging tool.

### JSON Format Description

Now we describe font mapping relationships directly using a JSON file. You only need to create a `font-faces.json` file with the following format:

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
| `urls` | Array of strings | Yes | - | Font file path, relative to the directory where the JSON file is located |

Further explanations for key fields are provided below.

**The `weight` Field**

For `weight`, input the CSS font weight numerical value directly, which will be rounded to the nearest standard value:

- `100` Thin
- `400` Regular (default value, can be omitted)
- `700` Bold
- `900` Black

**`urls` Path Resolution**

Paths in `urls` are resolved relative to the directory where the JSON file is located. For example, if the JSON file is located at `/fonts/font-faces.json`, writing `"fonts/NotoSans-Regular.ttf"` in `urls` will ultimately resolve to `/fonts/fonts/NotoSans-Regular.ttf`.

Therefore, it is recommended to place the JSON file directly in the same directory as the font files so that URLs can just use the file names. For example, the directory layout:

```
/fonts/
    font-faces.json
    NotoSans-Regular.ttf
    NotoSansSC-Regular.ttf
    NotoSans-Bold.ttf
```

In this case, the JSON content is as shown in the code above.

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

This is the only API call change; the rest of the code remains unchanged. Afterward, you can directly edit `font-faces.json` to add/remove fonts or adjust mapping relationships, without needing any conversion tools.

## FAQ

**How to handle multiple variants (like Regular, Bold, Italic) for the same family?**

Add independent entries for each variant in the `font-faces` array, distinguished by `weight` and `style`:

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

MCU projects typically only use the Regular `sans-serif` font with `normal` weight, and the system will fall back automatically.

**Can the `urls` array contain multiple files? When is it needed?**

Yes. When a font family needs to cover multi-language characters, put multiple font files into the same `urls` array. For example, `sans-serif` needs to support Latin letters, CJK characters, and Arabic simultaneously:

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

When rendering text, the engine will look up character glyphs in these files sequentially, and the first matched glyph will be used.

**Must the font files be in the same directory as the JSON?**

No. Paths in `urls` are resolved relative to the directory where the JSON file is located, so you can use relative paths to place fonts in subdirectories. Absolute paths can also be used, in which case they are unaffected by the JSON directory.

**Can a JSON string be passed directly in the code?**

Yes. Use the two-parameter overloaded version:

```cpp
map.readJSON("/fonts/", R"({
  "font-faces": [
    {"family": "sans-serif", "urls": ["NotoSans-Regular.ttf"]}
  ]
})");
```

The first parameter is `baseUri`, used to resolve relative paths in `urls`.