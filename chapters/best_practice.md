# 🚀 Best Practice
*just some unofficial notes*

Every design decision affects the total number of nodes and the complexity of the runtime model. Striking a balance between reusability, modularity, and performance is key, always considering the target hardware where the project will be deployed.

## Handling Node Count
- [ ] PLC variables are counted as nodes at the start of the Runtime, always import only variables that you need to exchange with the HMI.
- [ ] Each dynamic link = at least 3 OPC UA nodes
    - [ ] The materialized property node (no longer inherited from its base type).
    - [ ] The link node represents the connection.
    - [ ] The target node receiving the linked value
- [ ] Minimize converters (especially when nested) and nested dynamic links
- [ ] Avoid complex links in reused/high-traffic objects
- [ ] Prefer aliases over dynamic links in same container

Each dynamic link adds at least 2-3 extra references, and complex dynamic links (e.g., converters, expressions, switch-case logic) may add dozens. More references = slower traversal and resolution time.
(see [Diagnostic Tools](#7-diagnostic-tools))

## Image & Graphic Optimization
- [ ] PNGs are lighter to render, SVGs offer greater flexibility
- [ ] Optimize/compress PNGs
- [ ] Avoid large/uncompressed images
- [ ] Balance performance and quality
- [ ] Use stylesheets and single dynamic links for styles

## Reducing Overhead
- [ ] Replace complex dynamic links with NetLogics to centralize data processing
- [ ] Aggregate shared variables across multiple objects to reduce redundancy.

## Dynamic Object Management
- [ ] Avoid preloading unnecessary UI objects
- [ ] Use NetLogic for dynamic instantiation/lazy loading
- [ ] Instantiate objects only when needed: avoid using "Visible" property

[Reference: Creating Objects](https://github.com/FactoryTalk-Optix/NetLogic_CheatSheet/blob/main/pages/creating-objects.md#iuaobjects)

## Project Structure
- [ ] Store all graphics in the UI folder, organized by Templates/Screens
- [ ] Use a single EmbeddedDatabase with multiple tables if needed
- [ ] Place global variables in the Model folder
- [ ] Use Panels to group items for permissions/logic

## Naming Rules
- [ ] Use meaningful names for all project elements (avoid defaults, numbers, abbreviations)
- [ ] Use PascalCase for object names, camelCase for variables
- [ ] Use English for object names and localization keys
- [ ] Avoid using Panel+Rectangle for backgrounds; use Screen, Rectangle, or Panel as appropriate

See the full list: [Good Practices](https://github.com/FactoryTalk-Optix/NetLogic_CheatSheet/blob/main/pages/good-practices.md)

## Diagnostic Tools
- [ ] Project information
    - [ ] When you open the project in IDE the Studio Output will provide you with the actual number of nodes of the project. The message will contain the path of the project following the nodes count. In the same way, if you open with a text editor the project file with extension “.optix” you will find at the end of the file, the statistics of the project
- [ ] Use NodesCounterDialog widget
    - [ ] Identify high node count pages
    - [ ] Detect bottlenecks
    - [ ] Analyze elements for optimization
