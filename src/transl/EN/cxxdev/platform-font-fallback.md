# Platform Font Fallback

The Glyphix framework has a built-in font loading and fallback mechanism based on `font-face` / `font-family`. However, target platforms usually come with comprehensive font pipelines (such as Windows DirectWrite and macOS CoreText) that have already implemented system font fallback and related optimizations.

To make full use of the platform font pipeline, Glyphix allows you to take over font fallback: when the fonts within the framework cannot cover a certain character, the task is handed over to the platform to find and render a suitable system font. This article is intended for Glyphix system developers and will guide you step-by-step through the integration process.

Involved public header files:
- `gx_unite.h`: Contains UniTE public interfaces and the engine installation function `installEngine()`;
- `gx_shapingadapter.h`: This is the primary interface;
- `gx_fontdriver.h`: Provides the `FontDriver` encapsulation mechanism;
- `gx_fontloader.h`: Provides the font loader interface.

## General Concept

For a piece of text to be displayed on the screen, it goes through the following pipeline: Application text is handed over to the **paragraph layout engine** for line breaking and positioning; text with the same script and direction in each paragraph is **shaped** into glyphs; missing characters are filled in by **font fallback**; glyphs are then rendered into bitmaps by the **font driver**; and all fonts originate from the registration, loading, and reuse of the **font management** layer.

<ArchDiagram max-width="560px">
  <div>Application Text<div class="remark">Paragraph · String · Style</div></div>
  <div>
    Paragraph Layout Engine
    <div class="group row">
      <div>Lightweight Engine LiTE<div class="remark">Simple typesetting (Default engine)</div></div>
      <div>UniTE Engine<div class="remark">BiDi · Shape · Complex script</div></div>
    </div>
  </div>
  <div>
    Shaping · Font Fallback
    <div class="group row">
      <div>HarfBuzz<div class="remark">GSUB / GPOS</div></div>
      <div>Simple Shape<div class="remark">Character → Glyph</div></div>
      <div class="subject">FontFallbackShaper<div class="remark">family fallback · platform system font</div></div>
    </div>
  </div>
  <div>
    Font Rendering
    <div class="group row">
      <div>FontDriver<div class="remark">TTF / FreeType</div></div>
      <div>FontDriverFamily<div class="remark">Multi-face cascading</div></div>
      <div class="subject">PlatformFont Wrapper<div class="remark">Render platform fallback glyphs</div></div>
    </div>
    <div>GlyphCache - Glyph bitmap cache</div>
  </div>
  <div>
    Font Manager FontManager
    <div class="group row">
      <div>Registration / Lookup<div class="remark">face · family · properties</div></div>
      <div class="subject">FontLoader<div class="remark">Load face, inject wrapper</div></div>
    </div>
  </div>
</ArchDiagram>

The three highlighted parts in the diagram are covered in this article:
1. Fallback strategy `FontFallbackShaper`, used to find missing characters and perform fallback shaping;
2. `PlatformFont` wrapper responsible for rendering platform fallback fonts, used in conjunction with `FontFallbackShaper`;
3. `FontLoader` used to load the platform fallback font wrapper, which will be registered into the `FontManager`.

The remaining layers of the framework are already implemented. Text shaping (`ShapingAdapter`) generally does not need to be implemented from scratch; you can directly reuse the reference implementation.

### Prerequisites

Before implementing the platform font fallback feature according to this document, you need to:

- Enable the UniTE text engine (compared to the default lightweight engine, it supports complex script shaping and multi-level fallback).
- The target platform must support a complete font pipeline capable of providing advanced features such as system font shaping and script mapping. This is typically a complex subsystem that most MCU RTOS platforms lack.

::: important
Compared to the default LiTE engine, enabling UniTE and the complete font pipeline requires more memory and firmware space. Additionally, the performance of this engine is lower than that of the lightweight LiTE, so you need to evaluate whether it is necessary to enable it for full Unicode support and internationalization requirements.
:::

## Reusing the Shaping Backend

`ShapingAdapter` is responsible for shaping characters into glyphs. The built-in `HarfBuzzShaper` (`gx_harfbuzz_shaper.cpp`) implements full OpenType shaping by calling HarfBuzz, and then writes glyph indexes, advances, and offsets into the output based on target pixel sizes.

`HarfBuzzShaper` relies on FreeType to read font files, so both HarfBuzz and FreeType libraries must be included simultaneously. If these libraries already exist on the target platform, ensure version consistency; otherwise, linking or runtime errors may occur.

::: tip
Similar to HarfBuzz's [responsibilities](https://harfbuzz.github.io/what-harfbuzz-doesnt-do.html), `ShapingAdapter` does not handle text runs containing different fonts, which also includes the "font fallback" mechanism discussed below. Therefore, as long as the font used in shaping lacks a character, the `ShapingAdapter` implementation will return the `.notdef` glyph (index `0`), leaving it to be handled by the fallback strategy.
:::

## Implementing the Fallback Strategy

`FontFallbackShaper` is the core of the fallback mechanism. The engine calls it once for every shaped piece of text, requiring a glyph sequence **free of missing characters** as the shaping result. Unlike `ShapingAdapter`, it is not just for shaping a single font-face, but is designed for two-level fallback.

### Two-Level Fallback Cascading

`FontFallbackShaper::shape()` performs fallback in two levels from near to far:

- **Level 1**: Fill in missing characters within the current family using other fonts. This is already implemented by the framework; you only need to call `builtinShape()`.
- **Level 2**: Missing characters that cannot be resolved by Level 1 are handed over to the platform system fonts. This level is implemented by you.

Missing characters are represented in the data by a glyph index of `0`, i.e., `.notdef`. The return value of `shape()`, `FallbackResult`, uses bit flags to express the outcome: `result & NotNeeded` being true indicates that there are no more missing characters and processing can end directly; otherwise, common returns are `FullyResolved` (all processed) or `PartiallyResolved` (some `.notdef` characters remain).

### Skeleton of the `shape()` Function

First, call Level 1; return if there are no missing characters, otherwise proceed to Level 2 platform font fallback. `m_shaper` is the `ShapingAdapter` held by this fallback shaper (usually `HarfBuzzShaper`).

```cpp
FallbackResult shape(GlyphRunBundle &storage,
                     TextSpan text,
                     FontDriver *font) override {
    // Level 1: Use builtin API to handle fallback within the family
    auto r = builtinShape(storage, text, font, &m_shaper);
    if (r & NotNeeded)
        return r;                                  // No missing characters, finish
    return resolveByPlatform(storage, text, font); // Level 2, see below
}
```

`builtinShape()` is the only place that depends on `ShapingAdapter`. In this case, you typically implement `PlatformFallbackShaper` as follows:
```cpp
class PlatformFallbackShaper : public FontFallbackShaper {
    HarfBuzzShaper m_shaper; // Directly define as a member variable, no pointer reference needed

public:
    PlatformFallbackShaper() = default;
    FallbackResult shape(GlyphRunBundle &storage,
                         TextSpan text, FontDriver *font) override;
};
```
Note that `m_shaper` is merely a private member variable of your platform fallback strategy and does not need to be exposed to the outside. Inside `shape()`, simply pass `&m_shaper` when calling `builtinShape()`.

::: tip
In extreme cases (such as the initial adaptation phase), you can ignore fallback within the family, skip `builtinShape()`, and only handle Level 2 platform fallback. In this case, the `m_shaper` member variable can be omitted.

Regardless, specific `ShapingAdapter` classes generally cannot be defined as local variables because they may hold HarfBuzz cache states; recreating them on every shaping operation would cause severe performance degradation.
:::

### Obtaining Platform Fonts

Level 2 hands over missing characters to the platform and ultimately lets the wrapper render them. `fallbackFont(font)` returns the wrapper registered at the end of the family (see below). Its static type is `FontDriver *`, and you need to cast it back to your own wrapper type in order to call your custom registration and query interfaces.

```cpp
// Casting can also be done using dyn_cast, but if there is only one wrapper type, static_cast is also safe
auto *wrapper = static_cast<PlatformFont *>(fallbackFont(font));
if (wrapper == nullptr)
    return PartiallyResolved; // No wrapper at the end of the family, cannot continue
```

::: warning Must Be Implemented in Pairs
The fallback strategy and the wrapper are a matched pair: the `static_cast` above requires that `fallbackFont()` returns precisely your own wrapper type. Make sure that the installed fallback shaper matches the registered wrapper.
:::

### Simple Fallback Shaping

The most common and starter-friendly scenario is: an entire run can be shaped using a single platform font (i.e., a certain system font file completely covers the script). In this case, select the platform font according to `storage.run().spec.script`, reshape the entire run, write the entire run with the same `faceId`, and **directly overwrite the Level 1 result** without merging with already resolved glyphs.

UniTE splits runs by script, and Latin and CJK within the same text are naturally different runs. When the primary font focuses on Latin and encounters scripts like CJK, Arabic, or Devanagari, the run after `builtinShape()` is often entirely `.notdef`; reshaping and overwriting the entire run does not lose any already resolved glyphs. Therefore, the vast majority of multilingual typesetting follows this path and it is not a degenerate special case.

```cpp
// Select platform font according to script (platform font handle, not FontDriver), register to get faceId
auto sysFont = platformFontForScript(storage.run().spec.script);
uint32_t faceId = wrapper->registerFont(sysFont);
// Your shaping step yields glyphCount glyphs (demonstrated here with HarfBuzz output)
auto &run = storage.resize(glyphCount);
for (int i = 0; i < glyphCount; ++i) {
    run.data.glyphIds[i]   = GlyphIds::encodeFallback(gid[i], faceId);
    run.data.xAdvances[i]  = uint16_t(scale(pos[i].x_advance));
    run.data.xOffsets[i]   = int16_t(scale(pos[i].x_offset));
    run.data.yOffsets[i]   = int16_t(scale(pos[i].y_offset));
    run.data.clusterMap[i] = static_cast<int>(info[i].cluster);
}
```

The `pos`, `info`, `gid`, and `scale` fields come from your shaping steps, demonstrated above using HarfBuzz output.

::: tip Platform Shaping Capabilities
Platforms usually come with built-in shaping capabilities (such as DirectWrite, CoreText); whether to reuse HarfBuzz depends on the specific platform. The HarfBuzz output in the demonstration can be replaced with platform shaping output. For RTL runs (`spec.bidiLevel & 1`), the direction must be passed to the shaper.
:::

The prerequisite for this method is that the entire run maps to a single platform font. It is **not applicable to Common scripts** (Emojis, symbols, etc.): different characters within the same run may belong to multiple platform fonts, requiring the complex fallback described below.

### Complex Fallback Shaping

When multiple platform fonts are needed within a run, or only some clusters need fallback, the simple approach is no longer applicable. Considering that specific fallback and merging algorithms depend on platform APIs, this document only specifies the semantics that the merged `GlyphRun` must satisfy, and the implementation must handle them accordingly:

- Glyphs already resolved in Level 1 are **retained as-is**, and Level 2 only replaces clusters that are still `.notdef`.
- Fill every glyph slot with `glyphIds`, `xAdvances`, `xOffsets`, `yOffsets`, and `clusterMap`; fallback glyphs are marked using `encodeFallback(gid, faceId)`.
- `clusterMap[i]` is the offset of the source code point corresponding to this glyph relative to **this run** (consistent with `spec.text`, range `[0, text.length())`), used for drawing remapping and line clipping.
- Glyph count is variable: use `storage.resize()/reset()` to adjust storage, and then write slot by slot. `GlyphRunBundle` will automatically update `run().glyphCount`.
- When a single source cluster maps to multiple glyphs, the order and the sum of advances must be correct; code points swallowed by GSUB clustering should yield zero-advance glyphs to avoid gaps or misalignments.
- `faceId` must be a wrapper-registered ID that is stable throughout its lifecycle; the glyph order and shaping direction of RTL runs must be consistent.
- Return value: return `FullyResolved` if all are filled, or `PartiallyResolved` if residuals remain.

As long as the output satisfies the above constraints, the framework can render correctly. Whether to query platform APIs section by section or reuse HarfBuzz to shape font-by-font can be chosen based on the platform.

### Line Height and Caching

Line height depends on **which font actually draws** each glyph. `builtinLineMetrics()` handles parts of the glyphs within the family; glyphs with fallback marks (`isFallback()`) query the wrapper for their system fonts' ascents and descents to be incorporated. Fallback glyphs are encoded in `GlyphIds` by `encodeFallback`, and their `fontIndex()` is the written `faceId`, based on which the corresponding platform font is retrieved from the wrapper.

```cpp
VerticalMetrics resolveLineMetrics(const GlyphIds *gids, int count,
                                   FontDriver *font) const override {
    // Handle glyphs within the family
    VerticalMetrics m = builtinLineMetrics(gids, count, font);
    // Handle platform fallback glyphs
    auto *wrapper = static_cast<PlatformFont *>(fallbackFont(font));
    if (wrapper == nullptr)
        return m;
    // For glyphs where gids[i].isFallback(), query asc/descent from the wrapper and incorporate into m
    for (auto gid : utils::span<const GlyphIds>(gids, count)) {
        if (!gid.isFallback())
            continue; // Process fallback glyphs only
        uint32_t faceId = gid.fontIndex(); // fontIndex() of fallback glyph is faceId
        auto face = wrapper->fontForFaceId(faceId); // Platform font handle (not FontDriver)
        if (face == nullptr)
            continue;
        m.ascent = max(face->ascender(), m.ascent);
        m.descent = min(face->descender(), m.descent);
    }
    return m;
}
```

You can also aggregate the fallback fonts of the entire line and query their asc/descent in one go to avoid querying glyph-by-glyph inside a loop.

`flush()` is used to release system fonts cached by the wrapper:

```cpp
void flush(FontDriver *font) override {
    if (auto *w = static_cast<PlatformFont *>(fallbackFont(font)))
        w->releaseFonts();
}
```

::: tip
`flush()` is called by the framework when a paragraph is destroyed or memory is low; please clean up platform resources held by the wrapper inside it.
:::

## Fallback Font `FontDriver` Wrapper

The wrapper is responsible for rendering the glyphs shaped in the previous step into bitmaps. It inherits from `FontDriver` and carries the `PlatformFallback` flag during construction, allowing the framework to recognize it as a fallback font.

```cpp
class PlatformFont : public FontDriver {
public:
    PlatformFont(const String &family, const FontAttribute &attr)
        : FontDriver(family, attr, Vector | PlatformFallback) {}
    // ... bitmapOf / metricsOf ...
protected:
    void requestHandler(int) override {}
};
```

This font wrapper is not used to load some font file (like `FontDriverTTF` does). Its role is to hand over fallback glyphs to the platform font pipeline for processing, while its internal implementation is opaque to Glyphix.

### Dual-Mode Query

The `code` received by the wrapper has two meanings, distinguished by the `CodeAsGlyphId` bit:

- **With mark**: Queried by glyph index, with the high bits carrying `faceId` and the low bits being the glyph index. Once decoded, it is routed to the corresponding platform font, and then `glyphId` is used to query the corresponding `GlyphBitmap`.
- **Without mark**: Unicode character query, fallback lookup by codepoint among registered platform fonts, converting internally to a glyph index before querying.

A common implementation of `bitmapOf()` is as follows:

```cpp
bool bitmapOf(uint32_t code, GlyphBitmap *bitmap) override {
    if (code & CodeAsGlyphId) { // By glyph index
        uint32_t faceId  = (code >> 16) & 0x3ff;
        uint32_t glyphId =  code & 0xffff;
        auto face = fontForFaceId(faceId); // Platform font handle (not FontDriver)
        return face && face->bitmapOf(glyphId, bitmap);
    }
    // Unicode character lookup; iterate registered fonts here, or use a more efficient mapping table
    for (auto *face : registeredFonts()) {
        uint32_t glyphId = face->glyphIndexOf(code);
        if (face->bitmapOf(glyphId, bitmap))
            return true;
    }
    return false;
}
```

::: tip
`fontForFaceId()` returns a platform font handle, **not a `FontDriver`**; `face->bitmapOf(...)` and `face->glyphIndexOf(...)` above are pseudo-code for operations on that handle, representing "getting `GlyphBitmap` by `glyphId`" and "getting `glyphId` by codepoint" respectively.
:::

`metricsOf()` uses the same dual-mode logic; `advancesOf()`, `baseline()`, etc., are also calculated from platform fonts. `duplicate()` only needs to copy a mapping table.

### `faceId` Mapping

The wrapper maintains a mapping from `faceId` to platform fonts for use by the fallback strategy during registration and lookup during rendering.

`faceId` is a $10$-bit integer ($[0, 1023]$), and its meaning is entirely defined by the implementation. The only requirement is that it is **stable throughout its lifecycle**. There are two common approaches:

- **Fixed by script**: Directly use the `Script` enum value as `faceId`. The wrapper holds corresponding platform fonts by script, and registers them by script upon startup without runtime allocation.
- **Allocated on demand**: Allocate the next index whenever a new platform font is encountered, maintaining a growing table.

Example of fixing by script (`faceId` is the script value):
```cpp
PlatformFontHandle fontForScript(Script script) {
    switch (script) {
    case Script::Han:    return sysHanFont;
    case Script::Arabic: return sysArabicFont;
    case Script::Latin:  return sysLatinFont;
    // ...
    }
    return sysDefaultFont;
}
```
You need to handle script-to-font mapping, `faceId` allocation, and platform font object caching yourself.

::: tip
`faceId` is the contract between the fallback strategy and the wrapper: `PlatformFallbackShaper` uses it to encode glyphs, and `PlatformFont` uses it to decode back to system fonts. Both ends must interpret `faceId` consistently, and it must be representable by a $10\rm bit$ integer.
:::

## Registering the Wrapper

Finally, let the framework incorporate the wrapper into family loading. Implement `FontLoader::load()`, return a wrapper for a certain generic family name, and install it into the `FontManager`:

```cpp
struct PlatformFontLoader : public FontLoader {
    FontDriver *load(const String &face, const FontAttribute &attr) override {
        if (face == "sans-serif")
            return new PlatformFont(face, attr);
        return nullptr;
    }
};

CoreApp()->fontManager()->install(new PlatformFontLoader);
```

When an application requests a font in the form of `"<primary-face>,sans-serif"`, the framework merges the parts into the same family in comma-separated order, with the wrapper acting as the fallback face at the end, allowing `fallbackFont()` to retrieve it.

`PlatformFont` and `PlatformFontLoader` are usually only registered as fonts for generic family names like `sans-serif`, rather than specific system font names. This allows applications to use the same family name across different platforms without needing to know the specific fonts of the platform.

::: warning Functional Limitation
The wrapper relies on the application writing family names in the order described above, positioned as the last item in the family. Mechanisms to automatically guarantee this order are still under development.
:::

## Installation and Assembly

`installEngine()` in `gx_unite.h` connects your fallback strategy to the engine:

```cpp
unite::installEngine(*CoreApp()->typesetCore(),
                     std::make_unique<PlatformFallbackShaper>());
```

Complete assembly sequence:

1. `fontManager()->install(new PlatformFontLoader)`: Register the wrapper loader.
2. `installEngine(...)`: Install the fallback strategy holding the shaping backend.
3. Request fonts in the form of `"<primary-face>,sans-serif"`, layout, and draw as usual.

## Notes

- Advances / offsets are uniformly Q26.6 fixed-point (value = pixels × 64).
- Unresolved `.notdef` characters (glyph index $0$) are skipped during rendering, displaying blank spaces or tofu blocks at their corresponding positions.
- `faceId` is only $10$ bits, limiting the maximum number of simultaneously active system fonts in a single family to $1024$.
- The fallback strategy and the wrapper must be implemented in pairs and maintain type consistency (relying on `static_cast`).
- Be sure to release platform font caches held by the wrapper inside `flush()`.