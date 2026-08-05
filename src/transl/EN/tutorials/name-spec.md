---
icon: code-tags-check
---
# Component Naming Conventions

This document introduces the mandatory naming conventions and recommended naming styles for the component framework. Mandatory naming conventions are strictly required; failure to comply may result in unexpected behavior. Adhering to the recommended naming conventions ensures maximum compatibility.

## Template Naming Conventions

Tag names in templates must be in kebab-case or PascalCase:
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

It is recommended to uniformly use the kebab-case naming convention that complies with Web standards.

## JavaScript Code Naming Conventions


Component names in JavaScript code must be in PascalCase, while the corresponding kebab-case should be used in templates.

Component property names in JavaScript code must be in camelCase:
``` js
export default {
  data: {
    propName: 0 // The property name in the template is prop-name
  }
}
```
These property names are automatically converted to their corresponding kebab-case in template code.

## File Naming Conventions

UX files must use the same name as the component, which is PascalCase. In the `<import>` tag, the `src` attribute must be a case-sensitive file URL, and the `name` attribute must use either PascalCase or kebab-case:
``` html
<import src="path/to/UxFile" name="UxFile"/>
<import src="path/to/UxFile" name="ux-file"/>
```
In fact, the naming requirement for the `name` attribute is consistent with that of tag names in templates.