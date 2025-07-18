# 🚀 Best Practice for FTOptix

## 1. UI Design Principles
- [ ] Ensure UI is efficient and responsive
- [ ] Minimize the total node count per page
- [ ] Avoid unnecessary graphical elements
- [ ] Avoid unnecessary variables
- [ ] Avoid unnecessary dynamic links
- [ ] Use stylesheets instead of setting visual properties directly
- [ ] Use a single dynamic link to apply predefined styles when possible

## 2. Handling Node Count
- [ ] Understand each dynamic link = at least 3 OPC UA nodes
- [ ] Minimize use of expression-based converters
- [ ] Minimize use of key-value converters
- [ ] Minimize use of nested dynamic links
- [ ] Avoid complex dynamic links in frequently reused objects
- [ ] Avoid complex dynamic links in high-traffic or frequently accessed pages
- [ ] Prefer aliases over dynamic links within the same container

## 3. Image & Graphic Optimization
- [ ] Prefer SVG over PNG (vector-based, resolution-independent, editable at runtime)
- [ ] If using PNG, optimize and compress file size
- [ ] Avoid uncompressed or large images
- [ ] Balance rendering performance with visual quality

## 4. Reducing Overhead
- [ ] Replace complex dynamic links with scripts (NetLogic) for centralized processing
- [ ] Aggregate shared variables across objects to avoid duplication

## 5. Dynamic Object Management
- [ ] Avoid preloading unnecessary UI objects
- [ ] Use NetLogic scripts for dynamic instantiation
- [ ] Use NetLogic scripts for lazy loading
- [ ] Use NetLogic scripts for on-demand destruction/recreation
- [ ] Instantiate repetitive or hidden objects only when needed
- [ ] Reference: NetLogic_CheatSheet - [Creating Objects](https://github.com/FactoryTalk-Optix/NetLogic_CheatSheet/blob/main/pages/creating-objects.md#iuaobjects)

## 6. Diagnostic Tools
- [ ] Use the NodesCounterDialog widget
    - [ ] Identify pages with high node count
    - [ ] Detect performance bottlenecks
    - [ ] Analyze which elements need optimization