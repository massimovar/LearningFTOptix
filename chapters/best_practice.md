1. UI Design Principles
 Ensure UI is efficient and responsive

 Minimize the total node count per page

 Avoid unnecessary:

 Graphical elements

 Variables

 Dynamic links

 Use stylesheets instead of setting visual properties directly

 Use a single dynamic link to apply predefined styles when possible

2. Handling Node Count
 Understand each dynamic link = at least 3 OPC UA nodes

 Minimize use of:

 Expression-based converters

 Key-value converters

 Nested dynamic links

 Avoid complex dynamic links in:

 Frequently reused objects

 High-traffic or frequently accessed pages

 Prefer aliases over dynamic links within the same container

3. Image & Graphic Optimization
 Prefer SVG over PNG:

 Vector-based, resolution-independent

 Editable at runtime

 If using PNG:

 Optimize and compress file size

 Avoid uncompressed or large images

 Balance rendering performance with visual quality

4. Reducing Overhead
 Replace complex dynamic links with:

 Scripts (NetLogic) for centralized processing

 Aggregate shared variables:

 Across objects to avoid duplication

5. Dynamic Object Management
 Avoid preloading unnecessary UI objects

 Use NetLogic scripts for:

 Dynamic instantiation

 Lazy loading

 On-demand destruction/recreation

 Instantiate repetitive or hidden objects only when needed

 Reference: NetLogic_CheatSheet - Creating Objects

6. Diagnostic Tools
 Use the NodesCounterDialog widget:

 Identify pages with high node count

 Detect performance bottlenecks

 Analyze which elements need optimization