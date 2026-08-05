# C++ Learning Recommendations

This document is not a C++ tutorial; rather, it provides quick learning recommendations and prerequisite knowledge for developers preparing to read the documentation in this directory.

It assumes that you have long-term experience using C, and are familiar with MCUs, RTOS, drivers, LVGL, or similar embedded frameworks. You should have a wealth of programming experience, but may not be familiar with the subset of C++ required by Glyphix.

::: tip
If your goal is to develop Native Modules, asynchronous features, or Native Widgets, please read this document first before proceeding to the [Object System](./object-system.md) and other chapters. This will help you avoid many "I can understand the code, but I just can't write it" issues.
:::

## C++ Feature Subset

The Glyphix project disables certain C++ features, so developers do not need to learn them at all:

- **RTTI is disabled**: You cannot use `dynamic_cast`, `typeid`, or other runtime type identification mechanisms. When you need a safe downcast, use [`dyn_cast`](object-system.md#dynamic-type-casting) directly.
- **Exceptions are disabled**: You do not need to learn `try` / `catch` / `throw` as a primary path. Error handling should prioritize return values, status codes, object states, and explicit checks. This is similar to C error-handling conventions.


Additionally, the Glyphix runtime has some special constraints, which are mainly caused by the fragmentation and compatibility limitations of MCU systems:
1. Concurrency tools from the C++ standard library, such as `std::thread` and `std::mutex`, are not available on MCUs.
2. Time libraries like `std::chrono` are also not available on MCUs.
3. Do not use function-local static variables; the atomic initialization guaranteed since C++11 is **highly likely to be unreliable** on MCUs.
4. Do not use global variables (objects) that rely on heap allocation, because the global construction phase on MCUs may be uncontrolled, and heap memory might be unavailable.

Points 3 and 4 are very common scenarios and require special attention.

## C++ Knowledge to Master

The following content is sufficient to support most of the documentation in this directory.

### Classes and Object-Oriented Programming

You need to be able to at least read and write code like this:

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

- The difference between classes and structs (very little difference; mainly default access permissions)
- The meaning of public inheritance (generally, only public inheritance is used)
- Constructors and initialization lists
- Member functions, **`const` member functions**
- When a base class interface is being overridden versus when a normal member function is simply being declared

This knowledge will appear directly in the [Object System](./object-system.md), [Widget Development Guide](./widget.md), and [Widget Registration & Export](./widget-export.md).

### Pointers, References, and `const`

If you are familiar with C, this part is the easiest to "assume you already know," but C++ usage is stricter than C.

Key points that must be truly mastered:

- The difference between `T *` and `T &`
- When to pass by pointer versus when to pass by reference
- The meanings of **`const T *`**, `T *const`, and **`const T &`**
- Why `const` member functions are very common
- Why objects should not be arbitrarily manipulated byte-by-byte like in C

In Glyphix, this knowledge is directly related to interface design and lifecycle safety.

### Lifecycles and Resource Management

This is the most important section when migrating from C to C++.

You need to build the following habits:

- Objects are automatically destructed when they go out of scope.
- Constructors are responsible for establishing a valid state.
- Destructors are responsible for releasing resources.
- Do not manually clean up resources at the end of a function.
- Do not treat complex objects as ordinary memory blocks to be `memset` / `memcpy`'d.


A large number of Glyphix facilities and features are built on top of C++'s object lifecycle model, including topics such as RAII.

### Basic Usage of Templates

You don't need to understand this in depth, but you should at least be able to read:

- `Signal<int>`
- `Pointer<Label>`
- `SharedRef<MyData>`
- `async::ResultSession<Client>`
- `std::vector<T>`

And know that "templates are code generation mechanisms with type parameters," rather than some advanced trickery that only library authors touch.

In the Glyphix documentation, templates mainly appear in two forms:

- **Generic containers / utility types**, such as `Signal<T>`, `Pointer<T>`
- **Specialization points**, such as supplying `js_cast<T>` for custom types

Developers should at least understand basic terms like "template parameters," "instantiation," and "specialization," and be able to read template type declarations and usage. However, defining your own template classes or functions is not required.

### Lambda Expressions

In modern C++, lambdas are a very practical way to write one-off functions. You should at least be able to read:

```cpp
mod["double"] = [](JsCtx ctx) -> JsValue {
    return ctx.arg(0).asInt(0) * 2;
};
```

As well as:

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
Lambdas essentially completely occupy the niche of callback functions, meaning they are everywhere. To some extent, lambdas may be the most important C++ syntax point.

A **captureless** lambda expression is almost identical to a C function pointer, differing only in syntax and alleviating the "naming things is hard" problem.
:::

### Minimum Working Set of the Standard Library

You do not need to systematically study the entire STL, but it is recommended to first become familiar with these most common components:

- `std::vector`
- `std::array`
- `std::move`
- Basic algorithms from `<algorithm>`, iterators, and range-based `for` loops

::: tip Associative Containers
Glyphix implements its own `HashMap` and `HashSet`, which are very similar to `std::unordered_map`. However, using associative containers like `std::map` and `std::unordered_map` is not recommended due to their poor performance, and `std::map` suffers from noticeable code bloat.
:::

### C and C++ Interoperability

If you are interfacing with underlying SDKs, you will almost certainly use this part.

At a minimum, you should know:

- The purpose of `extern "C"`
- C callback function pointers
- `void *` context parameters, and the implicit conversion limitations of `void *` in C++
- The division of labor between C structs and C++ wrapper layers

You will see a very typical pattern in the [Async Development Examples](./async-examples.md): the C API handles the actual asynchronous execution, while the C++ layer only handles parameter wrapping, lifecycle management, and result passing.

::: tip Difficulty Expectation
This part is not difficult, but it is prone to linking errors. You may need to learn how to resolve issues caused by `extern "C"` and other factors when mixing C and C++ headers.
:::

## Recommended Learning Order

It is recommended to fill in the gaps in the following order, rather than reading a thick textbook from page one.

### First, Establish a "C to C++" Migration Perspective

[ISO C++ FAQ](https://isocpp.org/faq)
- Prioritize reading entries related to "Learning C++ if you already know C" and "How to mix C and C++."
- This material is well-suited for experienced C developers because it assumes you already understand memory, interfaces, building, and low-level constraints.

### Quickly Build an Impression of Modern C++

[A Tour of C++](https://www.stroustrup.com/Tour.html)
- If you are willing to read a short book, this is the one most worth investing time in.
- It is not a "zero-based programming tutorial," but rather a modern C++ overview for experienced developers.
- The goal is not to memorize everything, but to know what the main components of C++ are and what problems each solves.

### Syntax and Standard Library Reference Manual

[cppreference](https://en.cppreference.com/w/cpp)
- Suitable for looking things up as you go, rather than reading sequentially from cover to cover.
- When you encounter syntax or library names like `override`, lambdas, initialization lists, template specialization, or `std::vector` while reading the Glyphix documentation, you can look them up directly here.
- If you need to review certain details of the C language, you can also look them up here.

### Switch Your Coding Habits to Modern C++

[C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- This is not a tutorial, but rather a guide to engineering practices (also available in book form).
- Reading it sequentially from start to finish is not recommended; prioritize these chapters:
  - `P`: Philosophy
  - `I`: Interfaces
  - `F`: Functions
  - `C`: Classes and class hierarchies
  - `R`: Resource management
  - `ES`: Expressions and statements
  - `CPL`: Interop
  - `SF`: Source files
  - `SL`: The Standard Library
  - `CP`: Concurrency (read as needed)

[Embedded Artistry's C++ Articles](https://embeddedartistry.com/blog/tag/cpp/)
- Better suited for topical reading rather than a systematic course.
- Notable topics include how to use C++ without the heap, strong-type register encapsulation, and what happens before `main()`.

## How to Apply These Resources

A relatively efficient approach is not to "learn C++ for a while before starting Glyphix," but to proceed in parallel:

1. Read this document first to understand what knowledge needs to be supplemented.
2. Read [A Tour of C++](https://www.stroustrup.com/Tour.html) or the C-migration-related parts of the FAQ.
3. Start reading the [Object System](./object-system.md) and [Native Module Development](./native-module.md).
4. When you encounter syntax you don't understand, use [cppreference](https://en.cppreference.com/w/cpp) to look it up precisely.
5. When you encounter questions like "Why does modern C++ tend to be written this way?", refer to the corresponding chapters in the [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).

This learning rhythm is closer to real-world work and is better suited for developers who already have embedded experience.

## Mapping This Document to the cxxdev Documentation

If you are ready to continue reading, you can map the important knowledge points as follows:

- [Object System](./object-system.md): Classes, inheritance, lifecycles, references, template basics
- [SDK Project Setup](./sdk-setup.md): Header files, source files, build systems, basic class declaration knowledge
- [Native Module Development](./native-module.md): Function interfaces, lambdas, object lifecycles, C/C++ interop
- [Asynchronous Feature Development](./async.md): Templates, threading models, object ownership, callback constraints
- [Widget Development Guide](./widget.md): Inheritance, member functions, event handling, object trees, and the rendering pipeline