---
icon: code-tags-check
---
# Component naming convention

This document describes the mandatory naming conventions and recommended naming styles for component frameworks. Among them, the mandatory naming convention has mandatory requirements. If not followed, the effect may not meet the expectations. Using the recommended naming convention ensures maximum compatibility.

## Template naming convention

Tag names in templates must be kebab-case or PascalCase:
``` html
<Button></Button>
<button></button>
<scroll-area></scroll-area>
<ScrollArea></ScrollArea>
```

Attribute names must be dash or camelCase nomenclature:
``` html
<component prop-name="expr"></component>
<component propName="expr"></component>
```

It is recommended to use the dash nomenclature that complies with web standards.

## JavaScript code naming convention


Component names in JavaScript code must be Pascal naming, while the corresponding dash names are used in templates.

Component property names in JavaScript code must be camelCase:
``` js
export default {
  data: {
    propName: 0 // The attribute name in the template is prop-name
  }
}
```
These attribute names will be automatically converted into corresponding dash names in the template code.

## File name naming convention

The UX file must use the same name as the component, which is Pascal naming. In the `<import>` tag, the `src` attribute must be a case-sensitive file URL, and the `name` attribute should be named using Pascal naming or a dash:
``` html
<import src="path/to/UxFile" name="UxFile"/>
<import src="path/to/UxFile" name="ux-file"/>
```
In fact, the naming requirements of the `name` attribute are consistent with the tag names in the template.
