---
layout: dark
---

# 🚀 Performance optimizations

*just some unofficial notes*

---
- [Minimize the number of nodes](#minimize-the-number-of-nodes)
- [Reducing Overhead](#reducing-overhead)
- [Dynamic Object Management](#dynamic-object-management)
- [Image & Graphic Optimization](#image--graphic-optimization)
- [Diagnostic Tools](#diagnostic-tools)
---

Every design decision affects the total number of nodes and the complexity of the runtime model. Striking a balance between reusability, modularity, and performance is key, always considering the target hardware where the project will be deployed.

## Minimize the number of nodes
A well-structured UI must be efficient and responsive. A high number of nodes increases page load times and affects interface performance.

##### Suggestions

- [ ] PLC variables are counted as nodes at the start of the Runtime: always import only variables that you need to exchange with the HMI.

## Reducing Overhead

Each dynamic link adds at least 2-3 extra references, and complex dynamic links (e.g., converters, expressions, switch-case logic) may add dozens. More references = slower traversal and resolution time. Each dynamic link has at least 3 OPC UA nodes:

- The materialized property node (no longer inherited from its base type).
- The link node represents the connection.
- The target node receiving the linked value

##### Suggestions
- [ ] Minimize converters (especially when nested) and nested dynamic links
    - [ ] Replace complex dynamic links with NetLogics to centralize data processing
- [ ] Aggregate shared variables across multiple objects to reduce redundancy.
- [ ] Avoid complex dynamic links (converters) in reused/high-traffic objects
- [ ] Prefer aliases over dynamic links, where possible

## Dynamic Object Management

##### Suggestions
- [ ] Avoid preloading unnecessary UI objects
- [ ] Use NetLogic for dynamic instantiation/lazy loading
- [ ] Instantiate objects only when needed: avoid using "Visible" property

##### Why? How?

FT Optix renders and loads a page only when all its components are fully initialized. 

This means that if a page contains many preloaded objects, the system will take longer to process everything before displaying the UI. This can result in longer load times and a noticeable delay when switching between pages.

By using **dynamic instantiation with NetLogic scripts**, you can create and manage objects only when they are needed, instead of preloading everything at once. This approach is especially useful when dealing with repetitive elements, such as multiple instances of the same type of object that are only shown based on user interaction or external triggers.

One of the biggest benefits of this method is that it enables a form of **lazy loading**, where objects are instantiated while the page is already displayed and functional.
This results in:
- Faster initial page loads, as only the essential UI elements are rendered upfront.
- Smoother page transitions, since additional objects are loaded dynamically without delaying the page display.
- Better resource management, as objects can be destroyed and recreated on demand, reducing memory usage.

This method is particularly advantageous in scenarios where many UI elements would otherwise be hidden by default, such as complex dashboards, interactive lists, or modal pop-ups. 

Instead of keeping them in memory while hidden, you can **instantiate them only when required**, ensuring optimal performance.

[Reference: Creating Objects](https://github.com/FactoryTalk-Optix/NetLogic_CheatSheet/blob/main/pages/creating-objects.md#iuaobjects)

## Image & Graphic Optimization
##### Suggestions
- [ ] PNGs are lighter to render, SVGs offer greater flexibility (but "Advanced SVG Image" object can have a lot of dynamic links ...)
- [ ] Optimize/compress PNGs
- [ ] Avoid large/uncompressed images: balance performance and quality
- [ ] Use stylesheets and single dynamic links for styles

## Diagnostic Tools

### NodesCounterDialog widget (from the library)
- [ ] Identify high node count pages
- [ ] Detect bottlenecks
- [ ] Analyze elements for optimization

### Project information
When you open the project in IDE the Studio Output will provide you with the actual number of nodes of the project. The message will contain the path of the project following the nodes count. In the same way, if you open with a text editor the project file with extension “.optix” you will find at the end of the file, the statistics of the project.

##### How to Read
The dialog will display the following metrics:

##### Nodes Count
- Definition: Total number of nodes generated from this object in the OPC UA model. Includes objects, variables, methods, references, dynamic links, etc.
- Impact: This is the best indicator of the local complexity of the object. More nodes = heavier runtime load. If an object exceeds in number of nodes, its structure should be reviewed.
- Hint: You don’t need to create a single object that includes all possible information. Instead, you can use external objects such as dialogs or pop-ups to load additional content separately. With Aliases, you can exchange data between objects effectively while keeping the node count lower.
##### UI Objects Count
- Definition: Number of graphical components in the object (e.g., buttons, containers, labels, images).
- Impact: A high number of UI components increases rendering and rasterization load, especially on low-GPU hardware or high-resolution displays.
##### Variables Count
- Definition: Number of variables (properties) declared or used by the object.
- Impact: Static variables are light, but dynamic or calculated ones contribute to model size and memory usage. A large number of variables can reduce runtime responsiveness.
##### Dynamic Links Count
- Definition: Number of dynamic links connecting properties or variables to other nodes.
- Impact: Each dynamic link adds at least 3 nodes to the model and requires runtime resolution. Many links on the same object can slow down the loading or page transitions.
##### Converters Count
- Definition: Number of converters applied to properties or links (e.g., expression converters, key-value converters, conditional converters, etc.).
- Impact: Converters increase runtime computation, and each one can generate multiple additional nodes, especially when nested. Excessive use can create runtime bottlenecks.
- Hint: Sometimes converters refer to the same result or are applied to multiple properties. In these cases, consider creating a dedicated variable that holds the result of the expression, and then use a simple dynamic link to that variable instead of repeating the complex converter logic everywhere.