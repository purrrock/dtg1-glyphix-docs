---
icon: code-tags-check
---
# 组件命名规范

本文档介绍组件框架的强制命名规范以及建议的命名风格。其中强制命名规范强制性的要求，如果不遵守可能导致效果不符合预期。而使用推荐的命名规范则可以保证最大的兼容性。

## 模板命名规范

模板中的标签名称必须是短横线式（kebab-case）或者帕斯卡式（PascalCase）命名：
``` html
<Button></Button>
<button></button>
<scroll-area></scroll-area>
<ScrollArea></ScrollArea>
```

属性名称必须是短横线式或者驼峰式（camelCase）命名法：
``` html
<component prop-name="expr"></component>
<component propName="expr"></component>
```

推荐统一使用符合 Web 规范的短横线命名法。

## JavaScript 代码命名规范


JavaScript 代码中的组件名必须是帕斯卡命名，而模板中则使用对应的短横线命名。

JavaScript 代码中的组件属性名称必须是驼峰式命名：
``` js
export default {
  data: {
    propName: 0 // 在模板中的属性名是 prop-name
  }
}
```
这些属性名在模板代码中会自动转换成成对应的短横线命名。

## 文件名命名规范

UX 文件必须使用和组件相同的名字，也就是帕斯卡命名。在 `<import>` 标签中，`src` 属性（attribute）必须是区分大小写的文件 URL，而 `name` 属性则使用帕斯卡命名或者短横线命名：
``` html
<import src="path/to/UxFile" name="UxFile"/>
<import src="path/to/UxFile" name="ux-file"/>
```
实际上 `name` 属性的命名要求和模板中的标签名称是一致的。
