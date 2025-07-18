# 🚀 Best Practice
*just some unofficial notes*

## 1. UI Design Principles
- [ ] Ensure UI is efficient and responsive
- [ ] Minimize node count per page
- [ ] Avoid unnecessary graphics, variables, and dynamic links
- [ ] Use stylesheets and single dynamic links for styles

## 2. Handling Node Count
- [ ] Each dynamic link = at least 3 OPC UA nodes
- [ ] Minimize converters and nested dynamic links
- [ ] Avoid complex links in reused/high-traffic objects
- [ ] Prefer aliases over dynamic links in same container

## 3. Image & Graphic Optimization
- [ ] Prefer SVG over PNG
- [ ] Optimize/compress PNGs
- [ ] Avoid large/uncompressed images
- [ ] Balance performance and quality

## 4. Reducing Overhead
- [ ] Use scripts (NetLogic) for complex logic
- [ ] Aggregate shared variables

## 5. Dynamic Object Management
- [ ] Avoid preloading unnecessary UI objects
- [ ] Use NetLogic for dynamic instantiation/lazy loading
- [ ] Instantiate objects only when needed
- [ ] [Reference: Creating Objects](https://github.com/FactoryTalk-Optix/NetLogic_CheatSheet/blob/main/pages/creating-objects.md#iuaobjects)

## 6. Project Structure & Naming Rules

- [ ] Use meaningful names for all project elements (avoid defaults, numbers, abbreviations)
- [ ] Use PascalCase for object names, camelCase for variables
- [ ] Store all graphics in the UI folder, organized by Templates/Screens
- [ ] Use a single EmbeddedDatabase with multiple tables if needed
- [ ] Place global variables in the Model folder
- [ ] Use HTML color names (e.g., `red`), avoid hex unless needed
- [ ] Use English for object names and localization keys
- [ ] Sort items by type in the project tree
- [ ] Use Panels to group items for permissions/logic
- [ ] Match Label names and LocalizationDictionary keys
- [ ] Use keywords in control names to clarify purpose (e.g., `VoltageText`, `VoltageValue`)
- [ ] Avoid using Panel+Rectangle for backgrounds; use Screen, Rectangle, or Panel as appropriate

See the full list: [Good Practices](https://github.com/FactoryTalk-Optix/NetLogic_CheatSheet/blob/main/pages/good-practices.md)

## 7. Diagnostic Tools
- [ ] Use NodesCounterDialog widget
    - [ ] Identify high node count pages
    - [ ] Detect bottlenecks
    - [ ] Analyze elements for optimization
