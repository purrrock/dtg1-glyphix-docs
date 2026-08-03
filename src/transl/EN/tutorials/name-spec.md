---
icon: code-tags-check
---
# Component Naming Conventions

This document describes the mandatory naming conventions and recommended naming styles for the component framework. Mandatory naming conventions are strict requirements, and non-compliance may lead to unexpected behavior. Using the recommended naming conventions ensures maximum compatibility.

## Template Naming Conventions

Tag names in templates must be named in kebab-case or PascalCase:
``` html
<Button></Button>
<button></button>
<scroll-area></scroll-area>
<ScrollArea></ScrollArea>
```

Attribute names must be in kebab-case or camelCase:
``` html
<component prop-name="expr"></component>
<component propName="expr"></component>
```

It is recommended to consistently use kebab-case, which aligns with Web standards.

## JavaScript Code Naming Conventions

Component names in JavaScript code must use PascalCase, while the corresponding kebab-case names are used in templates.

Component property names in JavaScript code must use camelCase:
``` js
export default {
  data: {
    propName: 0 // The attribute name in the template is prop-name
  }
}
```
These property names will automatically be converted to the corresponding kebab-case names in template code.

## File Naming Conventions

UX files must use the same name as the component, which means PascalCase. In the `<import>` tag, the `src` attribute must be a case-sensitive file URL, while the `name` attribute uses PascalCase or kebab-case:
``` html
<import src="path/to/UxFile" name="UxFile"/>
<import src="path/to/UxFile" name="ux-file"/>
```
In fact, the naming requirements for the `name` attribute are consistent with the tag names in templates.