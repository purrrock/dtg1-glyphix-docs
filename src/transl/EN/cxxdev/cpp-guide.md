# C++ Learning Recommendations

This document is not a C++ tutorial, but rather a set of quick learning recommendations to provide prerequisite knowledge for developers preparing to read the documents in this directory.

It assumes that you have long-term experience using C, and are familiar with MCUs, RTOS, drivers, LVGL, or similar embedded frameworks; you should have extensive programming experience, but may not be familiar with the subset of C++ required by Glyphix.

::: tip
If your goal is to develop Native Modules, asynchronous features, or Native Widgets, please read this article first before proceeding to the [Object System](./object-system.md) and other chapters. This will help you avoid many issues where "the code makes sense, but you just can't write it."
:::

## C++ Feature Subset

The Glyphix project disables certain C++ features, so developers do not need to learn them at all:

- **RTTI** is disabled: You cannot use `dynamic_cast`, `typeid`, or other runtime type identification mechanisms. When you need a safe downcast, use [`dyn_cast`](object-system.md#动态类型转换) directly.
- **Exceptions** are disabled: There is no need to learn `try` / `catch` / `throw` as a primary path. For error handling, prioritize return values, status codes, object states, and explicit checks. This is similar to C error-handling habits.


In addition, the Glyphix runtime has some special constraints, mainly caused by the fragmentation and compatibility limitations of MCU systems:
1. Concurrency tools from the C++ standard library, such as `std::thread` and `std::mutex`, are not available on MCUs.
2. Time libraries such as `std::chrono` are also not available on MCUs.
3. Do not use function-local static variables. The atomic initialization guaranteed since C++11 is **highly likely to be unreliable** on MCUs.
4. Do not use global variables (objects) that rely on heap allocation, because the global construction phase on MCUs may be uncontrolled, and heap memory may not be available.

Among these, points 3 and 4 are very common scenarios and require special attention.

## C++ Knowledge to Master

The following content is sufficient to support most of the documentation in this directory.

### Classes and Object-Oriented Programming

You should at least be able to read and write code like this:

```cpp
class MyWidget : public Widget {
public:
    explicit MyWidget(Widget *parent = nullptr)
        : Widget(parent) {}

    void setValue(int value);
    int value() const;
};
```

You need to understand:

- The difference between classes and structs (not much difference, mainly default access permissions)
- The meaning of public inheritance (generally only public inheritance is used)
- Constructors and initialization lists
- Member functions, **`const` member functions**
- When you are overriding a base class interface versus just declaring a regular member function

This knowledge will appear directly in the [Object System](./object-system.md), [Widget Development Guide](./widget.md), and [Widget Registration and Export](./widget-export.md).

### Pointers, References, and `const`

If you are familiar with C, this part is the easiest to "assume you already know," but C++ usage is stricter than C.

Key points that must be truly mastered:

- The difference between `T *` and `T &`
- When to pass by pointer vs. when to pass by reference
- The meanings of **`const T *`**, `T *const`, and **`const T &`**
- Why `const` member functions are very common
- Why objects should not be arbitrarily processed byte by byte like in C

In Glyphix, this knowledge is directly related to interface design and lifecycle safety.

### Lifecycles and Resource Management

This is the most important section when migrating from C to C++.

You need to build the following habits:

- Objects are automatically destructed when they go out of scope.
- Constructors are responsible for establishing a valid state.
- Destructors are responsible for releasing resources.
- Do not put "resource cleanup" at the end of a function for manual handling.
- Do not treat complex objects as ordinary memory blocks to `memset` / `memcpy`.


A large number of Glyphix facilities and features are built on top of C++'s object lifecycle model, which includes topics such as RAII.

### Basics of Templates

You don't need to understand this deeply, but you must at least be able to read:

- `Signal<int>`
- `Pointer<Label>`
- `SharedRef<MyData>`
- `async::ResultSession<Client>`
- `std::vector<T>`

And know that "templates are code generation mechanisms with type parameters," rather than some advanced trick that only library authors touch.

In Glyphix documentation, templates mainly appear in two forms:

- **Generic containers/utility types**, such as `Signal<T>`, `Pointer<T>`
- **Specialization points**, such as supplying `js_cast<T>` for custom types

Developers should at least understand basic terminology such as "template parameters," "instantiation," and "specialization," and be able to read template type declarations and usages. However, defining your own template classes or functions is not required.

### Lambda Expressions

In modern C++, lambdas are a very practical way to write one-off functions. You should at least be able to read:

```cpp
mod["double"] = [](JsCtx ctx) -> JsValue {
    return ctx.arg(0).asInt(0) * 2;
};
```

And:

```cpp
int factor = readScaleFactorFromConfig();
mod["scale"] = [factor](JsCtx ctx) -> JsValue {
    return ctx.arg(0).asInt(0) * factor;
};
```

You should first become familiar with the basic syntax and capture mechanisms of lambdas, and focus on understanding:

- A lambda is an anonymous function object.
- A captureless lambda can often be used as a regular function pointer.
- A lambda with captures carries state.
- Once a lambda is held asynchronously, the lifecycle of the captured objects becomes critically important.

This directly affects code safety in [Native Module Development](./native-module.md) and [Async Development Examples](./async-examples.md).

::: tip Lambdas are very common
Lambdas effectively occupy the entire ecosystem of callback functions, meaning they are everywhere. To some extent, lambdas may be the most important C++ grammar point.

**Captureless** lambda expressions are almost equivalent to C function pointers, except for the syntax and the ability to alleviate "naming fatigue."
:::

### Minimum Working Set of the Standard Library

You don't need to systematically study the entire STL, but it is recommended to familiarize yourself with these most common parts:

- `std::vector`
- `std::array`
- `std::move`
- Basic algorithms `<algorithm>`, iterators, and range-based `for` loops

::: tip Associative Containers
Glyphix implements its own `HashMap` and `HashSet`, which are very similar to `std::unordered_map`. However, using associative containers like `std::map` and `std::unordered_map` is not recommended because their performance is poor, and `std::map` suffers from significant code bloat.
:::

### C and C++ Interoperability

If you are interfacing with underlying SDKs, you will almost certainly use this part.

You should at least know:

- The purpose of `extern "C"`
- C callback function pointers
- `void *` context parameters, and the implicit conversion limitations of `void *` in C++
- The division of labor between C structs and C++ wrapper layers

You will see a very typical pattern in the [Async Development Examples](./async-examples.md): the C API handles the actual asynchronous execution, while the C++ layer only handles parameter wrapping, lifecycle management, and result passing.

::: tip Difficulty Expectation
This part is not difficult, but it is very prone to link errors. You may need to learn how to resolve issues caused by `extern "C"` and others when mixing C and C++ headers.
:::

## Recommended Learning Order

It is recommended to fill in the gaps in the following order rather than reading a thick textbook from page one.

### First, Establish a "From C to C++" Migration Perspective

[ISO C++ FAQ](https://isocpp.org/faq)
- Prioritize reading entries related to "Learning C++ if you already know C" and "How to mix C and C++".
- This content is well-suited for experienced C developers because it assumes you already understand memory, interfaces, building, and underlying constraints.

### Quickly Build an Impression of Modern C++

[A Tour of C++](https://www.stroustrup.com/Tour.html)
- If you are willing to accept a short book, this is the most worthwhile one to invest time in.
- It is not a "zero-based programming tutorial," but a modern C++ overview for experienced developers.
- The goal is not to memorize everything, but to know what the main components of C++ are and what problems each solves.

### Syntax and Standard Library Reference Manual

[cppreference](https://en.cppreference.com/w/cpp)
- Suitable for looking things up as you go, not for reading sequentially from cover to cover.
- When you encounter syntax or library names like `override`, lambdas, initialization lists, template specialization, or `std::vector` while reading the Glyphix documentation, you can look them up here directly.
- If you need to review certain details of the C language, you can also look them up here.

### Switch Coding Habits to Modern C++

[C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- This is not a tutorial, but an engineering practice guide (there is also a published book version).
- Reading it cover-to-cover sequentially is not recommended; prioritize these sections:
  - `P`: Philosophy
  - `I`: Interfaces
  - `F`: Functions
  - `C`: Classes and class hierarchies
  - `R`: Resource management
  - `ES`: Expressions and statements
  - `CPL`: Interfacing with C
  - `SF`: Source files
  - `SL`: The Standard Library
  - `CP`: Concurrency (read as needed)

[Embedded Artistry's C++ Articles](https://embeddedartistry.com/blog/tag/cpp/)
- Better suited for topical reading rather than a systematic course.
- More noteworthy topics include: how to use C++ without the heap, strongly-typed register encapsulation, and what happens before `main()`.

## Recommended Way to Utilize These Resources

A more efficient approach is not to "learn C++ for a while before looking at Glyphix," but to do it in parallel:

1. Read this article first to know which knowledge needs to be supplemented.
2. Read [A Tour of C++](https://www.stroustrup.com/Tour.html) or the sections in the FAQ related to C migration.
3. Start reading the [Object System](./object-system.md) and [Native Module Development](./native-module.md).
4. When you encounter syntax you don't understand, use [cppreference](https://en.cppreference.com/w/cpp) for precise queries.
5. When you encounter questions like "Why does modern C++ tend to be written this way?", refer to the corresponding chapters in the [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).

This learning rhythm is closer to real work and better suited for developers with existing embedded experience.

## Mapping This Article to the cxxdev Documentation

If you are ready to continue reading, you can map the important knowledge points as follows:

- [Object System](./object-system.md): Classes, inheritance, lifecycles, references, template basics
- [SDK Project Configuration](./sdk-setup.md): Header files, source files, build systems, basic class declaration knowledge
- [Native Module Development](./native-module.md): Function interfaces, lambdas, object lifecycles, C/C++ interoperability
- [Async Feature Development](./async.md): Templates, threading models, object ownership, callback constraints
- [Widget Development Guide](./widget.md): Inheritance, member functions, event handling, object trees, and the rendering pipeline